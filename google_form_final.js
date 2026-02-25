function createFinalSurvey() {
  var form = FormApp.create("Japanese Sweets Survey");

  form.setDescription("Survey about Japanese snacks and packaging design. Thank you for your participation.");

  // Q1: パッケージの文字
  var q1 = form.addMultipleChoiceItem();
  q1.setTitle("Q1. Which do you prefer for text on snack packaging?");
  q1.setChoiceValues([
    "Original Japanese text",
    "Translated into my language",
    "Both languages displayed"
  ]);
  q1.setRequired(true);

  // Q2: 富士山と東京タワー
  var q2 = form.addMultipleChoiceItem();
  q2.setTitle("Q2. If Mt. Fuji and Tokyo Tower appeared together on a snack package design, would it feel odd to you?");
  q2.setChoiceValues([
    "Yes, it feels odd",
    "Slightly odd",
    "Not particularly odd",
    "It actually feels very Japanese and appealing"
  ]);
  q2.setRequired(true);

  // Q3: 買いたいお菓子
  var q3 = form.addCheckboxItem();
  q3.setTitle("Q3. Which snacks would you definitely buy when visiting Japan? (Select all that apply)");
  q3.setChoiceValues([
    "KitKat (regional limited flavors)",
    "Tokyo Banana",
    "Shiroi Koibito (White Lover)",
    "ROYCE Chocolate",
    "Pocky",
    "Matcha-flavored snacks",
    "Traditional Japanese sweets (mochi, senbei, etc.)",
    "Other"
  ]);
  q3.setRequired(true);

  // Q3 その他
  var q3other = form.addTextItem();
  q3other.setTitle("If you selected 'Other' in Q3, please specify:");
  q3other.setRequired(false);

  // Q4: 知ったきっかけ
  var q4 = form.addCheckboxItem();
  q4.setTitle("Q4. How did you learn about the snacks you selected? (Select all that apply)");
  q4.setChoiceValues([
    "Social media (Instagram, TikTok, YouTube, Xiaohongshu, etc.)",
    "Recommendations from friends or family",
    "Travel guidebooks or travel websites",
    "TV shows, movies, or dramas",
    "Saw them at supermarkets or convenience stores in my country",
    "Learned about them during a previous trip to Japan",
    "Other"
  ]);
  q4.setRequired(true);

  // Q4 その他
  var q4other = form.addTextItem();
  q4other.setTitle("If you selected 'Other' in Q4, please specify:");
  q4other.setRequired(false);

  // Q5: 紗々の認知
  var q5 = form.addMultipleChoiceItem();
  q5.setTitle("Q5. Do you know the Japanese chocolate 'SASHA' (紗々)?");
  q5.setChoiceValues([
    "Yes, I know it",
    "I have only heard the name",
    "No, I don't know it"
  ]);
  q5.setRequired(true);

  // Q6: 紗々のイメージ
  var q6 = form.addParagraphTextItem();
  q6.setTitle("Q6. [For those who know SASHA] What impression or image do you have of SASHA?");
  q6.setRequired(false);

  // ページ区切り: 属性情報
  form.addPageBreakItem().setTitle("About You");

  // 居住国
  var country = form.addMultipleChoiceItem();
  country.setTitle("Country of Residence");
  country.setChoiceValues([
    "South Korea",
    "China",
    "Thailand",
    "United States"
  ]);
  country.setRequired(true);

  // 年齢
  var age = form.addMultipleChoiceItem();
  age.setTitle("Age");
  age.setChoiceValues([
    "Under 20 (Teens)",
    "20-29",
    "30-39",
    "40-49",
    "50 and above"
  ]);
  age.setRequired(true);

  // 性別
  var gender = form.addMultipleChoiceItem();
  gender.setTitle("Gender");
  gender.setChoiceValues([
    "Male",
    "Female",
    "Other / Prefer not to say"
  ]);
  gender.setRequired(true);

  // 日本への渡航経験
  var visited = form.addMultipleChoiceItem();
  visited.setTitle("Have you ever visited Japan?");
  visited.setChoiceValues([
    "Yes",
    "No"
  ]);
  visited.setRequired(true);

  // 渡航回数
  var visitCount = form.addMultipleChoiceItem();
  visitCount.setTitle("[If Yes] How many times have you visited Japan?");
  visitCount.setChoiceValues([
    "1 time",
    "2-3 times",
    "4-5 times",
    "6 or more times"
  ]);
  visitCount.setRequired(false);

  // 確認メッセージ
  form.setConfirmationMessage("Thank you for completing this survey!");

  // URLをログとスプレッドシートに出力
  Logger.log("========================================");
  Logger.log("FORM CREATED SUCCESSFULLY!");
  Logger.log("========================================");
  Logger.log("Share this URL: " + form.getPublishedUrl());
  Logger.log("Edit form here: " + form.getEditUrl());
  Logger.log("========================================");

  var ss = SpreadsheetApp.create("Survey URLs");
  var sheet = ss.getActiveSheet();
  sheet.appendRow(["Share URL", form.getPublishedUrl()]);
  sheet.appendRow(["Edit URL", form.getEditUrl()]);
}
