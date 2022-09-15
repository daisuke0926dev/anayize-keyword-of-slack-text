import json
from array import array
import re



# json encorder
class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, FullyJson):
            return {'value': o.__dict__}
        if isinstance(o, Poster):
            return {'value': o.__dict__}
        if isinstance(o, Post):
            return {'value': o.__dict__}
        if isinstance(o, Reaction):
            return {'value': o.__dict__}
        if isinstance(o, Reply):
            return {'value': o.__dict__}
        return json.JSONEncoder.default(self, o)


# define fully json object
class FullyJson:
    # constructor
    def __init__(self, poster_name:str, poster_status:str, post_time:str, post_massage:str, reaction_array:array, reply_count:int):
        self.poster: Poster = Poster(poster_name, poster_status)
        self.post: Post = Post(post_time, post_massage)
        self.reply: Reply = Reply(reply_count)
        self.reaction_array = reaction_array


# define composition of json object
class Poster:
    # constructor
    def __init__(self, name:str, status:str):
        if type(name) is not str or type(status) is not str:
            raise TypeError('Error occured at Poster constructor')
        self.name = name
        self.status = status


class Post:
    # constructor
    def __init__(self, time:str, massage:str):
        if type(time) is not str or type(massage) is not str:
            raise TypeError('Error occured at Post constructor')
        self.time = time
        self.massage = massage

    def getMsg(self):
        print(self.massage)


class Reaction:
    # constructor
    def __init__(self, name:str, count:int):
        if type(name) is not str or type(count) is not int:
            raise TypeError('Error occured at Reaction constructor')
        self.name = name
        self.count = count


class Reply:
    # constructor
    def __init__(self, count:int):
        if type(count) is not int:
            raise TypeError('Error occured at Reply constructor')
        self.count = count


# is the number decimal
def isascnum(s):
    return True if s.isdecimal() and s.isascii() else False


def exchange():
    # main method start
    print("slack_text_to_json/main method is starting...")

    # get text data
    fully_data:str = open('./src/resource/slackText.txt', 'r', encoding="utf-8").read()

    # Leading Row Molding
    fully_data = '\n\n\n' + fully_data
    fully_data = re.sub("^\n+", "\n", fully_data)

    # Remove excessive blank lines of all rows(3 or more blanks remove)
    someblanks_removed_data_tmp=re.sub('\n\n\n+', '\n=====\n', fully_data)
    someblanks_removed_data=re.sub('\n+', '\n', someblanks_removed_data_tmp)

    # Forming to JSON format
    MAX_MENTION_LENGTH = 20
    LINE_OF_POSTER_NAME:int = 1
    LINE_OF_POSTER_STATUS_AND_TIME:int = 2
    LINE_OF_BEGINNING_MASSAGE_:int = 3

    #Break down it into posts.
    posting_data:array=[]
    contain_non_posting_data:array = someblanks_removed_data.split('=====')
    for data_may_be_posting in contain_non_posting_data:
        each_lines_of_post:str = data_may_be_posting.split('\n')
        # contain mm:ss on the line
        contain_time:bool = re.search('[0-9]{2}:[0-9]{2}',each_lines_of_post[LINE_OF_POSTER_STATUS_AND_TIME]) is not None
        if(contain_time):
            posting_data.append(data_may_be_posting)

    ret_arr:array = []
    for a_post in posting_data:
        # define roop meta data
        roop_count:int = 0
        be_skip:bool = False # this flg use for skipping non-post data like '~が参加しました'
        reaction_flg:bool = False # this flg use to get the next line reaction_count
        #define class member
        reaction_array:array = []
        reaction:Reaction = ("",0)
        poster_name:str = ''
        poster_status:str = ''
        post_time:str = ''
        post_massage:str = ''
        reaction_name:str = ''
        reaction_count:int = 0
        reply_count:int = 0
        
        for line in a_post.split('\n'):
            if(roop_count == 0): # cuz blank line
                pass
            elif(roop_count == LINE_OF_POSTER_NAME):
                poster_name = line
            elif(roop_count == LINE_OF_POSTER_STATUS_AND_TIME):
                if(line[0] == ':'):
                    poster_status = line.split()[0]
                    post_time = line.split()[1]
                else:
                    post_time = line.split()[0]
            else:
                if(len(line) < 1): # cuz blank line
                    pass
                #if the line is only :something: then the line is reaction-line
                elif(line[0] == ':' and line[-1:] == ':' and line.count(':') < 3):
                    reaction_name = line
                    reaction_flg = True
                elif(reaction_flg):
                    reaction_flg = False
                    if(isascnum(line)):
                        reaction_count = int(line)
                        reaction_array.append(Reaction(reaction_name,reaction_count))
                else:
                    if(line[0]=='@' and len(line) < MAX_MENTION_LENGTH):
                        post_massage += ' '+line
                    elif(' に追加されました。' in line or 'チャンネルのトピックを設定しました: ' in line or ' に参加しました。' in line):
                        be_skip = True
                    else:
                        post_massage += line
            roop_count += 1
        if(be_skip):
            pass
        elif(len(post_massage) == 0):
            pass
        else:
            # encoded data store in array for return
            fully_json:FullyJson = FullyJson(poster_name, poster_status, post_time, post_massage, reaction_array, reply_count)
            js = json.dumps(fully_json, cls=MyEncoder, ensure_ascii=False)
            ret_arr.append(js)
    print("...slack_text_to_json/main method is ending")
    return ret_arr