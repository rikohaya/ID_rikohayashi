function createJapaneseSweetsSurvey() {
  var form = FormApp.create("Japanese Sweets Survey");

  var q1 = form.addMultipleChoiceItem();
  q1.setTitle("Q1. Which do you prefer for text on snack packaging?");
  q1.setChoiceValues([
    "Original Japanese text",
    "Translated into my language",
    "Both languages"
  ]);
  q1.setRequired(true);

  var q2 = form.addMultipleChoiceItem();
  q2.setTitle("Q2. If Mt. Fuji and Tokyo Tower appeared together on a snack package, would it feel odd?");
  q2.setChoiceValues([
    "Yes, it feels odd",
    "Slightly odd",
    "Not particularly odd",
    "It feels very Japanese and appealing"
  ]);
  q2.setRequired(true);

  var q3 = form.addCheckboxItem();
  q3.setTitle("Q3. Which snacks would you buy when visiting Japan? (Select all that apply)");
  q3.setChoiceValues([
    "KitKat (regional limited flavors)",
    "Tokyo Banana",
    "Shiroi Koibito (White Lover)",
    "ROYCE Chocolate",
    "Pocky",
    "Matcha-flavored snacks",
    "Traditional Japanese sweets (mochi, senbei)",
    "Other"
  ]);
  q3.setRequired(true);

  var q3other = form.addTextItem();
  q3other.setTitle("If you selected Other in Q3, please specify:");
  q3other.setRequired(false);

  var q4 = form.addMultipleChoiceItem();
  q4.setTitle("Q4. How did you learn about these snacks?");
  q4.setChoiceValues([
    "Social media (Instagram, TikTok, YouTube)",
    "Friends or family",
    "Travel guides or websites",
    "TV shows, movies, dramas",
    "Saw them at local stores",
    "Previous trip to Japan",
    "Other"
  ]);
  q4.setRequired(true);

  var q5 = form.addMultipleChoiceItem();
  q5.setTitle("Q5. Do you know the Japanese chocolate SASHA?");
  q5.setChoiceValues([
    "Yes, I know it",
    "I have only heard the name",
    "No, I do not know it"
  ]);
  q5.setRequired(true);

  var q6 = form.addParagraphTextItem();
  q6.setTitle("Q6. (If you know SASHA) What impression do you have of it?");
  q6.setRequired(false);

  var country = form.addMultipleChoiceItem();
  country.setTitle("Country of Residence");
  country.setChoiceValues([
    "Korea",
    "China",
    "Thailand",
    "USA"
  ]);
  country.setRequired(true);

  var age = form.addMultipleChoiceItem();
  age.setTitle("Age");
  age.setChoiceValues([
    "Teens",
    "20s",
    "30s",
    "40s",
    "50+"
  ]);
  age.setRequired(true);

  var visited = form.addMultipleChoiceItem();
  visited.setTitle("Have you visited Japan?");
  visited.setChoiceValues([
    "Yes",
    "No"
  ]);
  visited.setRequired(true);

  Logger.log("Form URL: " + form.getPublishedUrl());
  Logger.log("Edit URL: " + form.getEditUrl());
}
