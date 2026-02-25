from fastapi import APIRouter, HTTPException
from backend.services import media_calculator
from backend.services.gemini import estimate_target_population
from backend.models import (
    MediaPlanCalculateRequest,
    MediaPlanCalculateResponse,
    MediaPlanReverseRequest,
    MediaPlanReverseResponse,
    MediaPlanOptionsResponse,
    TargetEstimateRequest,
    TargetEstimateResponse,
    CustomMediaPlanCalculateRequest,
    CustomMediaPlanReverseRequest,
    TargetAdCostRequest,
    TargetAdCostResponse,
    TargetAdCostPerMedia,
)

router = APIRouter(prefix="/api/media-plan", tags=["media-plan"])


@router.get("/options", response_model=MediaPlanOptionsResponse)
async def get_options():
    """利用可能なオプション（年齢層、性別、媒体、デフォルトCPM）を取得"""
    options = media_calculator.get_available_options()
    return options


@router.post("/calculate", response_model=MediaPlanCalculateResponse)
async def calculate(request: MediaPlanCalculateRequest):
    """通常計算: ターゲット × 媒体 → 費用算出"""
    try:
        result = media_calculator.calculate_normal(
            age_group=request.age_group,
            gender=request.gender,
            media=request.media,
            reach_rate=request.reach_rate,
            frequency=request.frequency,
            cpm=request.cpm,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reverse", response_model=MediaPlanReverseResponse)
async def reverse_calculate(request: MediaPlanReverseRequest):
    """予算逆算: 予算 → リーチ可能人数算出"""
    try:
        result = media_calculator.calculate_reverse(
            age_group=request.age_group,
            gender=request.gender,
            media=request.media,
            budget=request.budget,
            frequency=request.frequency,
            cpm=request.cpm,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/estimate-target", response_model=TargetEstimateResponse)
async def estimate_target(request: TargetEstimateRequest):
    """AIを使ってターゲットの推定人口を算出"""
    try:
        result = await estimate_target_population(
            target_description=request.target_description,
            media=request.media,
        )
        return {
            "target_description": request.target_description,
            **result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/custom-calculate", response_model=MediaPlanCalculateResponse)
async def custom_calculate(request: CustomMediaPlanCalculateRequest):
    """カスタムターゲット計算: 指定した人口で費用算出"""
    try:
        result = media_calculator.calculate_with_custom_population(
            target_population=request.target_population,
            media=request.media,
            reach_rate=request.reach_rate,
            frequency=request.frequency,
            cpm=request.cpm,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/custom-reverse", response_model=MediaPlanReverseResponse)
async def custom_reverse_calculate(request: CustomMediaPlanReverseRequest):
    """カスタムターゲット予算逆算: 指定した人口でリーチ可能人数算出"""
    try:
        result = media_calculator.reverse_with_custom_population(
            target_population=request.target_population,
            media=request.media,
            budget=request.budget,
            frequency=request.frequency,
            cpm=request.cpm,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/estimate-ad-cost", response_model=TargetAdCostResponse)
async def estimate_ad_cost(request: TargetAdCostRequest):
    """
    ターゲット像から「SNSで刺すためにかかる広告配信費」を一括計算。
    AIで推定人口 → リーチ率・フリークエンシーで費用見積。
    """
    try:
        media_list = (
            [request.media]
            if request.media
            else media_calculator.get_available_options()["media_types"]
        )
        # 1. AIでターゲット推定人口を取得（1媒体で代表取得）
        estimate_media = request.media or "Instagram"
        estimate_result = await estimate_target_population(
            target_description=request.target_description,
            media=estimate_media,
        )
        pop = estimate_result["estimated_population"]
        if pop <= 0:
            pop = 500_000  # フォールバック

        # 2. 各媒体で費用計算
        per_media = []
        for media in media_list:
            calc = media_calculator.calculate_with_custom_population(
                target_population=pop,
                media=media,
                reach_rate=request.reach_rate,
                frequency=request.frequency,
                cpm=request.cpm,
            )
            per_media.append(
                TargetAdCostPerMedia(
                    media=media,
                    estimated_cost=calc["estimated_cost"],
                    reach_count=calc["reach_count"],
                    total_impressions=calc["total_impressions"],
                    target_population=pop,
                    cpm_used=calc["cpm_used"],
                )
            )

        # 3. サマリメッセージ（最低・最高の目安）
        costs = [p.estimated_cost for p in per_media]
        min_c, max_c = min(costs), max(costs)
        summary = (
            f"「{request.target_description}」にSNSで刺すためには、"
            f"リーチ率{request.reach_rate}%・フリークエンシー{request.frequency}回の場合、"
            f"おおよそ {min_c:,}円〜{max_c:,}円（媒体により異なります）の広告配信費が見込まれます。"
        )

        return TargetAdCostResponse(
            target_description=request.target_description,
            estimated_population=pop,
            reasoning=estimate_result["reasoning"],
            confidence=estimate_result["confidence"],
            per_media=per_media,
            summary_message=summary,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
