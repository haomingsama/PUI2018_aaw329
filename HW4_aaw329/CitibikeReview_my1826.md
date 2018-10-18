## Citibike Review

The null and alternative hypotheses are formulated clearly, but perhaps too simple that it does not require a statistical test. All needs to be done is to count instances with age<40 and age>= 40 and then compare them (like you did in figure 1). No regression needed.

To make the question more interesting, I would like to propose a small change in the hypotheses. Instead of comparing the number of rides, compare the trip duration of those two age groups. Hence,

### Null hypothesis $$ H_0: TD_{age<40} <= TD_{age>=40} $$
### Alternative hypothesis $$ H_a: TD_{age<40} > TD_{age>=40} $$

where $TD_{age}$ refers to the trip duration of selected age group. 

You can fit a simple linear regression to test your hypotheses. But before you do that, you need to recode your age variable, because right now this is numerical, but you want it to be binary. For instance, you can assign age_group = 1 for all instances with age >= 40 and 0 if otherwise. Then after getting the regression result, you can consider performing a McNemar's test because your data is catagorical and paired. 

Reviewer: Muci Yu, my1826