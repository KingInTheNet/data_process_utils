from google.cloud import translate
import time
f = open('output2','r')
fout = open('out','w')
def detect_language(text):
    # [START translate_detect_language]
    """Detects the text's language."""
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    #print('Text: {}'.format(text))
    #print('Confidence: {}'.format(result['confidence']))
    #print('Language: {}'.format(result['language']))
    return result['language']
    # [END translate_detect_language]
def filter_vi(input):
    start = time.time()
    words = input.split()
    for word in words:
        try:
            s1=detect_language(word)
            if s1== "vi":
                return True
                break
            else:
                return False
            print("    "+str(time.time()-start))
        except Exception as e:
            print(e)
            return False

