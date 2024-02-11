import boto3
import json
from openai import OpenAI

boto3.setup_default_session(profile_name='my-dev-profile')
s3 = boto3.client('comprehendmedical', region_name='us-east-2')

data = """Pt is 19 years olf. Pt has migrane for past 10 hours. Pt is taking tylenol but it is not helping. 
Blurry Vision and pain in right eye are symptoms. Photophobia is a symptom.
Patient has a history of migranes which occur once a month. Patient is perscribed Imitrex.
Light and sound worsen symptoms. Movement worsens symptoms. Patient sometimes experieinces vomiting during migranes.
patient has migranes with aura. Patient denies any fever or. lightheadedness. Heart sounds normal with no murmurs, rubs or gallops.
PERRLA. EOMI. No cervical lymphadenopathy. Normal neuro exam. High BP. Differential Diagnosis inlcudes stroke and aneurysm.
Pt had a negativ CT scan 5 years ago so no repeat CT today. Diagnosis Migrane with aura. Pt was given a dose and a prescription of Rixatriptan."""

result = json.dumps(s3.detect_entities_v2(Text= data),sort_keys=True, indent=4)

client = OpenAI(api_key="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")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You will be generating sample written electronic medical records based on a dictionary of data provided by the user"},
    {"role": "assistant", "content": """
    Electronic Medical Record

    Patient Information:

    Age: 19
    Gender: Female

    Chief Complaint:
    Migraine for the past 10 hours.

    History of Present Illness:
    The patient presents with a severe migraine lasting for the past 10 hours.
    The pain is located in the right eye and is associated with blurry vision and photophobia.

    Physical Exam:
    Neurological: Normal neuro exam, PERRLA, EOMI.
    Cardiovascular: Heart sounds normal, no murmurs, rubs, or gallops detected.
    Respiratory: Clear breath sounds bilaterally.
    Musculoskeletal: No edema or deformity noted.
    Gastrointestinal: Vomiting.
    General: The patient appears uncomfortable due to migraine pain.
    Skin: Warm and dry, no rashes or lesions observed.
    Head and Neck: Cervical lymphadenopathy noted.

    Symptoms:
    Blurry vision.
    Pain in the right eye.
    Photophobia.
    Vomiting.
    Fever (denied).
    Lightheadedness (denied).
    Cervical lymphadenopathy.

    Differential Diagnosis:
    Inlcudes stroke (low confidence).
    Aneurysm (low confidence).

    Diagnostic Tests:
    CT scan performed 5 years ago, results negative.

    Diagnosis:
    Migraine with aura.

    Medications Perscribed:
    Rixatriptan for migraine.

    Follow-up:
    Monitor blood pressure.
    Reassess if symptoms persist or worsen.

    Signed:
    [Physician's Name]
    [Date]
    """},

    {"role": "user", "content": result}
  ]
)

print(result)
print(response['choices'][0]['message']['content'])

