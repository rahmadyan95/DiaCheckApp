import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
import pickle
import google.generativeai as genai
import os 

genai.configure(api_key='AIzaSyAxfJplG4PN9VlCA8Z1g-Ao__OX-scdCc8')

script_dir = os.path.dirname(os.path.abspath(__file__))
class prediction:

    def run_prediction(self):

        processing_0 = 'Reading Dataset'

        dataset_directory = os.path.join(script_dir,'diabetes_prediction_dataset.csv')

        df = pd.read_csv(dataset_directory)
        df = df.drop_duplicates()
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()

        processing_1 = 'Encoding Starting'

        df['gender'] = le.fit_transform(df['gender'])
        df['smoking_history'] = le.fit_transform(df['smoking_history'])
        self.features = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        
        processing_2 = 'Encoding Succesfull'
        
        X = df[self.features]
        y = df['diabetes']

        processing_2 = 'Standarization Dataset Starting'

        # Standardizing the features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        processing_3 = 'Standarization Dataset Successfull'

        # Applying PCA

        processing_4 = 'Dimentional Reduction Starting'

        self.pca = PCA()
        X_pca = self.pca.fit_transform(X_scaled)
        max_index = self.pca.explained_variance_ratio_.cumsum().argmax()
        n_components = max_index + 1
        self.pca = PCA(n_components=n_components)
        X_pca = self.pca.fit_transform(X_scaled)
        X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

        processing_5 = 'Dimentional Reduction Succesfull'

        # Initializing and training the XGBoost model

        processing_6 = 'Training Starting'

        self.xgb_model = XGBClassifier(random_state=42)
        self.xgb_model.fit(X_train, y_train)

        processing_6 = 'Training Sucessfull'

        # Making predictions
        y_pred = self.xgb_model.predict(X_test)

        # Evaluating the model
        accuracy = accuracy_score(y_test, y_pred)
        print(f'XGBoost Accuracy: {accuracy:.4f}')
        print(f'XGBoost Classification Report:\n{classification_report(y_test, y_pred)}')

        # Save the model
        with open('Diabetes_model.pkl', 'wb') as f:
            pickle.dump(self.xgb_model, f)


        return df.isna().sum(),accuracy,classification_report(y_test,y_pred)


    def create_data_tuple(self, gender, age,hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level):
    # Menyiapkan data input pengguna dalam bentuk list
        custom_data = [
            gender,
            age,
            hypertension,  # hypertension, asumsi default (mungkin perlu disesuaikan)
            heart_disease,
            smoking_history,
            bmi,
            HbA1c_level,
            blood_glucose_level
        ]

        # Convert to pandas DataFrame
        custom_df = pd.DataFrame([custom_data], columns=self.features)

        # Standardize the custom data
        custom_X = self.scaler.transform(custom_df[self.features])

        # Apply PCA transformation
        custom_X_pca = self.pca.transform(custom_X)

        # Make predictions using the trained XGBoost model
        custom_predictions = self.xgb_model.predict(custom_X_pca)

        # Print the predictions
        for i, pred in enumerate(custom_predictions):
            if pred == 0:
                print(f"Person {i+1} is not predicted to have diabetes.")
                return False
            else:
                print(f"Person {i+1} is predicted to have diabetes.")
                return True


class generative_text :
        
        
    def generate_suggestion(self,age,hypertension_status,heart_disaes_status,smoking_status,bmi,hb_level,glucose_level,status,lenght_word_cut):
        self.prompting = f'''I am {age} years old, with a hypertension status of {hypertension_status}, heart disease status of {heart_disaes_status}, 
    and smoking status of {smoking_status}. My BMI is {bmi}, my HbA1c level is {hb_level} with a glucose level of {glucose_level}, 
    and diabetes status is {status}. What should I do to stay health? (if status false that mean i didnt have diabetes)'''

        response = genai.generate_text(
            model="models/text-bison-001",
            prompt=self.prompting
        )

        generative_result = str(response.result)

    # Cleaning asteric
        cleaning_1 = generative_result.replace("*",'')

        formatted_text = ''
        line_length = lenght_word_cut
        words = cleaning_1.split()

        current_line = ''
        for word in words:
            if len(current_line) + len(word) + 1 <= line_length:
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word
            else:
                formatted_text += current_line + '\n'
                current_line = word

        # Add the last line
        if current_line:
            formatted_text += current_line

        return formatted_text


