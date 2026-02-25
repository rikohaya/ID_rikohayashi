function createCompleteSurvey() {
  var form = FormApp.create("Japanese Sweets Survey / 日本のお菓子に関するアンケート");

  form.setDescription("This survey is about Japanese snacks and packaging design. Thank you for your participation.\n\nこのアンケートは日本のお菓子とパッケージデザインに関する調査です。ご協力ありがとうございます。");

  // Q1: パッケージの文字 / Package text preference
  var q1 = form.addMultipleChoiceItem();
  q1.setTitle("Q1. Which do you prefer for text on snack packaging? / お菓子のパッケージに書かれている文字は、どちらが良いですか？");
  q1.setChoiceValues([
    "Original Japanese text / 日本語のまま",
    "Translated into my language / 母国語に翻訳されている方が良い",
    "Both languages / 両方表記されている方が良い"
  ]);
  q1.setRequired(true);

  // Q2: 富士山と東京タワー / Mt. Fuji and Tokyo Tower
  var q2 = form.addMultipleChoiceItem();
  q2.setTitle("Q2. If Mt. Fuji and Tokyo Tower appeared together on a snack package, would it feel odd? / お菓子のパッケージデザインに「富士山」と「東京タワー」が同時に描かれていたら、違和感を感じますか？");
  q2.setChoiceValues([
    "Yes, it feels odd / 違和感を感じる",
    "Slightly odd / 少し違和感を感じる",
    "Not particularly odd / 特に違和感はない",
    "It feels very Japanese and appealing / むしろ日本らしくて良い"
  ]);
  q2.setRequired(true);

  // Q3: 買いたいお菓子 / Snacks to buy (multiple choice)
  var q3 = form.addCheckboxItem();
  q3.setTitle("Q3. Which snacks would you definitely buy when visiting Japan? (Select all that apply) / 日本旅行に来たら絶対に買いたいお菓子はどれですか？（複数選択可）");
  q3.setChoiceValues([
    "KitKat (regional limited flavors) / キットカット（ご当地限定味）",
    "Tokyo Banana / 東京ばな奈",
    "Shiroi Koibito (White Lover) / 白い恋人",
    "ROYCE Chocolate / ロイズチョコレート",
    "Pocky / ポッキー",
    "Matcha-flavored snacks / 抹茶味のお菓子全般",
    "Traditional Japanese sweets (mochi, senbei, etc.) / 和菓子（もち、せんべい等）",
    "Other / その他"
  ]);
  q3.setRequired(true);

  // Q3 その他 / Q3 Other specification
  var q3other = form.addTextItem();
  q3other.setTitle("If you selected 'Other' in Q3, please specify: / Q3で「その他」を選んだ方は具体的に教えてください");
  q3other.setRequired(false);

  // Q4: 知ったきっかけ / How did you learn about these snacks
  var q4 = form.addCheckboxItem();
  q4.setTitle("Q4. How did you learn about the snacks you selected in Q3? (Select all that apply) / Q3で選んだお菓子を知ったきっかけは何ですか？（複数選択可）");
  q4.setChoiceValues([
    "Social media (Instagram, TikTok, YouTube, etc.) / SNS（Instagram, TikTok, YouTube等）",
    "Recommendations from friends or family / 友人・家族からの口コミ",
    "Travel guidebooks or travel websites / 旅行ガイドブック・旅行サイト",
    "TV shows, movies, or dramas / テレビ番組・映画・ドラマ",
    "Saw them at supermarkets or convenience stores in my country / 自国のスーパー・コンビニで見かけた",
    "Learned about them during a previous trip to Japan / 以前の日本旅行で知った",
    "Other / その他"
  ]);
  q4.setRequired(true);

  // Q4 その他 / Q4 Other specification
  var q4other = form.addTextItem();
  q4other.setTitle("If you selected 'Other' in Q4, please specify: / Q4で「その他」を選んだ方は具体的に教えてください");
  q4other.setRequired(false);

  // Q5: 紗々の認知 / SASHA awareness
  var q5 = form.addMultipleChoiceItem();
  q5.setTitle("Q5. Do you know the Japanese chocolate 'SASHA' (紗々)? / 日本のチョコレート「紗々（さしゃ）」を知っていますか？");
  q5.setChoiceValues([
    "Yes, I know it / 知っている",
    "I have only heard the name / 名前だけ聞いたことがある",
    "No, I don't know it / 知らない"
  ]);
  q5.setRequired(true);

  // Q6: 紗々のイメージ / SASHA impression
  var q6 = form.addParagraphTextItem();
  q6.setTitle("Q6. [For those who answered 'Yes' or 'I have only heard the name' in Q5] What impression do you have of SASHA? / 【Q5で「知っている」「名前だけ聞いたことがある」と答えた方】紗々にどのようなイメージを持っていますか？");
  q6.setRequired(false);

  // セクション: 属性情報 / Demographics section
  form.addPageBreakItem().setTitle("Demographics / 属性情報");

  // 居住国 / Country of Residence
  var country = form.addMultipleChoiceItem();
  country.setTitle("Country of Residence / 居住国");
  country.setChoiceValues([
    "South Korea / 韓国",
    "China / 中国",
    "Thailand / タイ",
    "United States / アメリカ",
    "Other / その他"
  ]);
  country.setRequired(true);

  // 居住国その他 / Country Other
  var countryOther = form.addTextItem();
  countryOther.setTitle("If you selected 'Other' for Country, please specify: / 居住国で「その他」を選んだ方は具体的に教えてください");
  countryOther.setRequired(false);

  // 年齢 / Age
  var age = form.addMultipleChoiceItem();
  age.setTitle("Age / 年齢");
  age.setChoiceValues([
    "Under 20 / 10代",
    "20-29 / 20代",
    "30-39 / 30代",
    "40-49 / 40代",
    "50 and above / 50代以上"
  ]);
  age.setRequired(true);

  // 性別 / Gender
  var gender = form.addMultipleChoiceItem();
  gender.setTitle("Gender / 性別");
  gender.setChoiceValues([
    "Male / 男性",
    "Female / 女性",
    "Other / その他",
    "Prefer not to say / 回答しない"
  ]);
  gender.setRequired(true);

  // 日本への渡航経験 / Have you visited Japan
  var visited = form.addMultipleChoiceItem();
  visited.setTitle("Have you ever visited Japan? / 日本への渡航経験はありますか？");
  visited.setChoiceValues([
    "Yes / あり",
    "No / なし"
  ]);
  visited.setRequired(true);

  // 渡航回数 / Number of visits
  var visitCount = form.addMultipleChoiceItem();
  visitCount.setTitle("[If you answered 'Yes' above] How many times have you visited Japan? / 【「あり」と答えた方】日本への渡航回数は？");
  visitCount.setChoiceValues([
    "1 time / 1回",
    "2-3 times / 2〜3回",
    "4-5 times / 4〜5回",
    "6 or more times / 6回以上"
  ]);
  visitCount.setRequired(false);

  // 今後の訪日予定 / Future visit plans
  var futurePlan = form.addMultipleChoiceItem();
  futurePlan.setTitle("Do you plan to visit Japan in the future? / 今後日本に行く予定はありますか？");
  futurePlan.setChoiceValues([
    "Yes, within 1 year / はい、1年以内に",
    "Yes, within 2-3 years / はい、2〜3年以内に",
    "Someday, but no specific plans / いつか行きたいが具体的な予定はない",
    "No plans / 予定はない"
  ]);
  futurePlan.setRequired(true);

  // 自由コメント / Free comments
  var freeComment = form.addParagraphTextItem();
  freeComment.setTitle("Any other comments about Japanese snacks? / 日本のお菓子について、その他ご意見があればお聞かせください");
  freeComment.setRequired(false);

  // 確認メッセージ設定
  form.setConfirmationMessage("Thank you for completing this survey!\n\nアンケートにご協力いただき、ありがとうございました！");

  // URLをログに出力
  Logger.log("===========================================");
  Logger.log("Form created successfully!");
  Logger.log("===========================================");
  Logger.log("Response URL (share this): " + form.getPublishedUrl());
  Logger.log("Edit URL (for editing): " + form.getEditUrl());
  Logger.log("===========================================");

  // スプレッドシートにも出力（見やすくするため）
  var ss = SpreadsheetApp.create("Survey URLs - Japanese Sweets");
  var sheet = ss.getActiveSheet();
  sheet.appendRow(["Form Name", "Japanese Sweets Survey"]);
  sheet.appendRow(["Response URL (share this)", form.getPublishedUrl()]);
  sheet.appendRow(["Edit URL (for editing)", form.getEditUrl()]);
  sheet.appendRow(["Created", new Date()]);

  Logger.log("URLs also saved to spreadsheet: " + ss.getUrl());
}
