import pickle

# open a file, where you stored the pickled data
file = open('scraped_data.pkl', 'rb')

# dump information to that file
data = pickle.load(file)

# close the file
file.close()

print(data)