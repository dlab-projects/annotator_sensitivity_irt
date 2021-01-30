# Measuring Hate Speech: Applications to Fairness in Machine Learning

This repo contains the code and documentation for D-Lab's Fairness in Machine Learning project, that is part of the larger online hate speech project. See the previous [repo](https://github.com/dlab-projects/hatespeech-2019) for the ["Constructing interval variables via faceted Rasch measurement and multitask deep learning: a hate speech application"](https://arxiv.org/abs/2009.10277) preprint.

# Paper Outline

This outline is preliminary and will likely change as the project develops.

**Research Question**: Do general models of online hate speech achieve sub-group fairness for the target populations?

- Introduction
    - Summary of preprint
    - Framing problem of fairness of hate speech models working at scale
- Literature Review
- Exploratory Data Analysis
    - Distributions of labeler characteristics v. labels of hate speech measures
    - Validation of IRT in achieving first-order debiasing 
    - Distribution of target identities within our dataset
- Model Auditing
    - Counterfactual fairness
        - Would hate speech score be the same if target identity was changed?
    - Reclaimed Speech
        - Dictionary of reclaimed phrases 
- Conclusion
    - IRT as a method for improving bias introduced by human labelers
    - Validation of labels through counterfactual analysis
    - Areas for improvement suggested by audit  

# Repository Structure

This is a draft repository structure that can be modified as the project develops.

- **exploratory-data-analysis**:
    - /renata/
        - hs_notebook.ipynb
        - **Note**: This was copied from the hatespeech-2019 repo
- **modeling**:
    - /aniket/
        - counterfactual_fairness.ipynb
        - reclaimed_speech_analaysis.ipynb

# Repository Notes

- Files should operate based on the main repository directory being the current working directory. That will ensure that script paths work for any team member.
- Best to avoid committing binary files (data, images, etc.). These can quickly inflate the repo size and are more likely to yield merge conflicts.
- Data can be stored in google drive and then manually copied into the repository structure, and vice versa, without being committed to the git repo.

# TODO

- [ ] Literature Review
- [ ] EDA
- [ ] Research resign for assessing counterfactual fairness
- [ ] Research design for assessing errors in reclaimed speech
- [ ] Additional Labeling 