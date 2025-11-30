import os
import json
import time
from datetime import datetime

class FeedbackAnalyzer:
    """
    A simple feedback analyzer that performs basic sentiment analysis.
    """
    def __init__(self):
        self.positive_words = {
            'good', 'great', 'excellent', 'awesome', 'fantastic', 'love', 
            'nice', 'best', 'amazing', 'helpful', 'useful', 'perfect', 
            'outstanding', 'brilliant', 'wonderful', 'superb', 'impressive',
            'easy', 'intuitive', 'smooth', 'fast', 'reliable', 'enjoyable',
            'like', 'works', 'cool', 'fine', 'decent'
        }
        self.negative_words = {
            'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 
            'poor', 'boring', 'useless', 'broken', 'confusing', 'difficult',
            'frustrating', 'annoying', 'disappointing', 'slow', 'buggy',
            'complicated', 'crashes', 'freezes', 'laggy', 'unreliable',
            'problem', 'issue', 'error', 'fix', 'improve'
        }

    def analyze_feedback(self, text):
        """
        Analyze the given feedback text and return sentiment analysis results.
        """
        if not text or not text.strip():
            return {'status': 'error', 'message': 'empty feedback text'}
        
        text_lower = text.lower()
        
        # count positive and negative words
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        # determine sentiment
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # calculate sentiment score
        total_words = positive_count + negative_count
        if total_words > 0:
            sentiment_score = (positive_count - negative_count) / total_words
        else:
            sentiment_score = 0.0
        
        return {
            'status': 'success',
            'sentiment': sentiment,
            'sentiment_score': round(sentiment_score, 3),
            'positive_words_found': positive_count,
            'negative_words_found': negative_count,
            'word_count': len(text.split()),
            'character_count': len(text)
        }

def process_feedbacks():
    """
    Monitor and process feedbacks in the json file.
    """
    analyzer = FeedbackAnalyzer()
    json_file = "feedbacks.json"
    
    print("feedback analysis service started")
    print("monitoring for new feedbacks...(press ctrl+c to stop)")
    
    try:
        while True:
            # check if json file exists
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        feedbacks = json.load(f)
                    
                    # find unanalyzed feedbacks
                    unanalyzed = [f for f in feedbacks if f.get('status') == 'pending']
                    
                    if unanalyzed:
                        print(f"found {len(unanalyzed)} new feedback(s) to analyze")
                        
                        # analyze each pending feedback
                        for feedback in unanalyzed:
                            feedback_text = feedback.get('feedback', '')
                            
                            if not feedback_text:
                                print("  empty feedback, skipping")
                                continue
                            
                            # analyze the feedback
                            analysis_result = analyzer.analyze_feedback(feedback_text)
                            
                            # update feedback with analysis
                            feedback['status'] = 'analyzed'
                            feedback['analysis'] = analysis_result
                            feedback['analyzed_at'] = datetime.now().isoformat()
                            
                            # display result
                            sentiment = analysis_result['sentiment']
                            score = analysis_result['sentiment_score']
                            pos = analysis_result['positive_words_found']
                            neg = analysis_result['negative_words_found']
                            print(f"  analyzed: {sentiment} (score: {score:.3f}, +{pos}/-{neg} words)")
                        
                        # save updated feedbacks back to file
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(feedbacks, f, indent=2, ensure_ascii=False)
                        
                        print("  all feedbacks analyzed and saved")
                    
                except Exception as e:
                    print(f"error processing feedbacks: {e}")
            
            # wait before checking again
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nfeedback analysis service stopped")

if __name__ == '__main__':
    process_feedbacks()