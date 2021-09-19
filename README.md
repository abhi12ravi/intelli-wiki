# IWPPA (Intelligent Wikipedia Page Protection Assistant)
An assistant for Wikipedia administrators that predicts the protection level and protection duration as per Wikipedia's page protection policy.

## Goals of this assistant

Using state-of-the-art machine learning techniques:
1. Predict protection_level of a given Wikipedia article
2. Predict the protection_duration for the said article 

## Steps to run the file
1. Install all dependencies mentioned in the requirements.txt file
2. Run the `scripts/get_titles.py` file to fetch all Wikipedia titles
3. Run the `scripts/get_data.py` file to fetch all data for a given title
4. Run: `$python .\scripts\get_features_all_pages.py .\dataset\trial_unbalanced\titles_unprotected.csv .\dataset\trial_unbalanced\collected_features.csv 0` to get all features. The second parameter is the input csv file containing 
5. Run the `scripts/make_predictions.py` file to apply machine learning algorithms and get predictions.
6. `Demo.py` instantiates the Gradio user interface and hosts a local webapp.

## Credits 
1. [Abhijeet Lokhande](https://gitlab.com/abhijeetlokhande1996)

## References
1. [DePP 2016](https://dl.acm.org/doi/10.1145/2983323.2983914)
2. [Detecting pages to protect in Wikipedia across multiple languages 2019](https://link.springer.com/article/10.1007/s13278-019-0555-0)
