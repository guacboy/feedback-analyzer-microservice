# Feedback Analyzer Microservice

## How to REQUEST Data (Submit Feedback)

### Method 1: Programmatic Submission

Write feedback data directly to `feedbacks.json` in the microservice folder:

```python
import json
import os
from datetime import datetime

def submit_feedback(feedback_text):
    """
    Submit feedback by writing to the feedbacks.json file in the microservice folder.
    """
    microservice_folder = "feedback-analyzer-microservice"
    json_filepath = os.path.join(microservice_folder, "feedbacks.json")
    
    # create the folder if it doesn't exist
    os.makedirs(microservice_folder, exist_ok=True)
    
    # prepare feedback data
    feedback_data = {
        'timestamp': datetime.now().isoformat(),
        'feedback': feedback_text,
        'status': 'pending' # mark as pending analysis
    }
    
    # read existing feedbacks or create new list
    if os.path.exists(json_filepath):
        try:
            with open(json_filepath, 'r', encoding='utf-8') as f:
                all_feedbacks = json.load(f)
        except:
            all_feedbacks = []
    else:
        all_feedbacks = []
    
    # add new feedback
    all_feedbacks.append(feedback_data)
    
    # write back to file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_feedbacks, f, indent=2, ensure_ascii=False)
    
    print(f"feedback submitted to: {json_filepath}")

# example usage
submit_feedback("this app is amazing and very helpful for studying!")
```

### Method 2: Manual File Editing

Manually edit the `feedbacks.json` file to add new feedback:

```json
[
  {
    "timestamp": "2024-12-01T14:30:22.123456",
    "feedback": "The interface could use some improvements",
    "status": "pending"
  }
]
```

## How to RECEIVE Data (Access Analysis Results)

### Starting the Microservice

1. Run the microservice:
   ```bash
   cd feedback-analyzer-microservice
   python feedback.py
   ```

2. The microservice will:
   - Start monitoring `feedbacks.json` for new feedbacks with status "pending"
   - Analyze each pending feedback using sentiment analysis
   - Update the JSON file with analysis results
   - Display real-time updates in the console

### Reading Analysis Results

```python
import json
import os

def get_analyzed_feedbacks():
    """
    Read all analyzed feedbacks from the JSON file.
    """
    microservice_folder = "feedback-analyzer-microservice"
    json_filepath = os.path.join(microservice_folder, "feedbacks.json")
    
    if os.path.exists(json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as f:
            feedbacks = json.load(f)
        
        # filter only analyzed feedbacks
        analyzed_feedbacks = [f for f in feedbacks if f.get('status') == 'analyzed']
        return analyzed_feedbacks
    else:
        return []

# example usage
results = get_analyzed_feedbacks()
for feedback in results:
    print(f"Feedback: {feedback['feedback']}")
    print(f"Sentiment: {feedback['analysis']['sentiment']}")
    print(f"Score: {feedback['analysis']['sentiment_score']}")
    print(f"Positive words: {feedback['analysis']['positive_words_found']}")
    print(f"Negative words: {feedback['analysis']['negative_words_found']}")
    print("---")
```

## Example Output

### Console Output (Microservice)
```
feedback analysis service started
monitoring for new feedbacks...
press ctrl+c to stop
found 1 new feedback(s) to analyze
  analyzed: positive (score: 1.000, +2/-0 words)
  all feedbacks analyzed and saved
```

### JSON Output (feedbacks.json)
```json
[
  {
    "timestamp": "2024-12-01T14:30:22.123456",
    "feedback": "This app is amazing and very helpful!",
    "status": "analyzed",
    "analysis": {
      "status": "success",
      "sentiment": "positive",
      "sentiment_score": 1.0,
      "positive_words_found": 2,
      "negative_words_found": 0,
      "word_count": 6,
      "character_count": 34
    },
    "analyzed_at": "2024-12-01T14:30:25.123456"
  }
]
```