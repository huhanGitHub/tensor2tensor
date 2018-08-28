import json
count=0
api_seq_file=open('api_seq.txt','a+')
comment_file=open('comment.txt','a+')
with open('train.json') as f:
    for line in f:
        count=count+1
        if count<=200000:
            line=line.strip()
            #print(line)
            line=json.loads(line)
            api_seq=line['api_seq']
            comment=line['comment']
            #print(comment)
            #print(api_seq)
            api_seq_file.write(str(api_seq)+'\n')
            comment_file.write(str(comment)+'\n')
        else:
            break
f.close()
api_seq_file.close()
comment_file.close()