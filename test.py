import pickle

# open a file, where you stored the pickled data
file = open('scraped_data.pkl', 'rb')

# dump information to that file
submission = pickle.load(file)

# close the file
file.close()

counter = 0
for comment in submission.comments:
    counter+=1

print(submission.num_comments)
