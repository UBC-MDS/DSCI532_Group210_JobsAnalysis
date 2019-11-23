### Motivation and Purpose

Diversity has been shown consistently by research to be conducive to increased innovation, productivity, and employee engagement in a company. It brings more perspectives, thereby enabling teams to make more thorough and creative decisions. Furthermore, it upgrades a company's reputation, allowing it to connect with the community on a deeper level.

For many industries, the most critical benchmark for achieving diversity is through gender. Historically, different jobs have had various degrees of gender balance, and they are still evolving today. Despite this progress, there are still a lot more male-dominated occupations than balanced or female-dominated groups. Therefore, there are still lots of room for improvement. For researchers or any other stakeholders looking to improve gender balance in specific industries, it is essential to explore and compare the historical trends on gender balance in relevant jobs in order to find insights on obstacles, identify good and bad examples on gender balance, and get guidance on directing future research efforts.

We propose building an application that makes this exploration possible. In particular, this web application will provide dashboards that portray historical trends of different job gender groups, such as male-dominated, female-dominated, or male-only jobs, and how specific jobs' gender proportions have evolved. Users will be able to see the general trends and track their progress as well as look more deeply into the jobs they are interested in and see how their gender balances have changed. They will be able to identify problems, draw comparisons, and find valuable clues that inform them further on how to improve gender balance in specific industries.

### Description of the data

In this project, we will be visualizing the gender makeup of job workforces from 255 different jobs between the years 1850 and 2000. Each of the 7650 workforces in our data have 5 associated variables that describe their job name (`job`), the binary sex of the workforce (`sex`), the decade their information was collected (`year`), and the proportion of the workforce to that of the decade's total workforce (`perc`). Using this data, we will also derive two new variables for each workforce. The first is the dominant sex of that workforce's job in that decade (`gender_dominant_group`), and it is based on the ratio of men to women in that job in that decade (only male, male dominant, balanced, female dominant, only female). The second is the proportion of the workforce to that of their job's total workforce in that decade (`annual_gender_prop_in_job`).

### Research questions and usage scenarios

- Naomi is a researcher in a reputable HR consulting company that regularly score substantial contracts from sizable companies on how to grow or restructure their workforce so that they can continue to feel engaged, creative, productive and proud of the company. As a result, often times, Mary and her team will be tasked with researching the gender diversity of various industries because achieving gender balance is usually a crucial part of most projects for helping companies build towards a more robust work culture.

- Naomi and her colleges want to be able to explore historical data on gender balance of various occupations in order to gain insights on the history of gender diversity in certain industries and devise theories on why they were less than optimal. They also want to identify industry leaders on gender balance and learn from them.

- When Naomi and her team of researchers goes on our website, they will be able to explore the historical trends of job gender groups and compare how different jobs' gender diversities have evolved.

- With the societal view of job gender group trends, the team can try to understand about how gender diversity in the entire job market has changed and hypothesize about how historical events have impacted the rise or fall of different job gender groups. These insights could be highly relevant to how today's society is influencing gender balance in the workforce.

- With the job-specific view of gender ratio changes over time, the team can look at how the industries of their clients have fared over time on gender inclusivity. They can also explore how some extreme examples of different gender dominated groups have evolved over time on their gender balance and investigate the historical gender diversity of whatever jobs they find relevant to their projects.
