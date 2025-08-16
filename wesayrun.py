from simulation import simulation
import gensim.downloader as api

def run():
    
    wv = api.load('glove-twitter-25')

    for _ in range(2):
        print(simulation(wv=wv))

if __name__ == "__main__":
    run()