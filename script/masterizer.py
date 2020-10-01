

def main():
    logging.info("----- Masterizer script by akaRicane -----")

    fs, data = read(filePath=filePath)

    fft = scipy.fft.fft(data)

    plt.plot(fft)
    plt.show()


    logging.info("---- End of the program ----")

if __name__ == "__main__":
    a = numpy.ones(10)
    print(a)