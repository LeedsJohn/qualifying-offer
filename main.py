import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

class Offer:
    """
    Class to represent data revolving around qualifying offers for departing
    free agent players.
    """
    def __init__(self, year, minSalary, maxSalary, link):
        """
        Constructor - receives:
        integer year (current year)
        integer minSalary (minimum reasonable salary)
        integer maxSalary (maximum reasonable salary)
        string link (link to dataset)
        """
        self.year = str(year)
        self.minSalary = minSalary # track min and max salary to ensure data is reasonable
        self.maxSalary = maxSalary
        self.soup = self.getSoup(link)
        # {"name": integer salary}
        self.salaries = {} # assuming no players with identical names and salaries
        self.errors = [] # names of players who fail data validation

    def getSoup(self, link):
        """
        Receives link to dataset
        Returns beautiful soup object
        """
        req = requests.get(link)
        return BeautifulSoup(req.content, "html.parser")

    def getSalaries(self):
        """
        Iterates through every entry of player data
        Either adds the player to self.salaries or self.errors, depending
        on whether they pass data validation.
        """
        for entry in self.soup.find_all("tr"):
            name = entry.find(class_ = "player-name").text
            salary = self.salaryToInt(entry.find(class_ = "player-salary").text)
            year = entry.find(class_ = "player-year").text
            level = entry.find(class_ = "player-level").text.upper()
            if self.validateEntry(name, salary, year, level):
                self.salaries[name] = salary
            else:
                self.errors.append(name)
    
    def salaryToInt(self, stringSalary):
        """
        Converts a string salary to an integer.
        Returns an integer salary value if possible, else -1
        Note: Ignores all characters after a period - cents are not
        worth considering.
        """
        salary = ""
        for c in stringSalary:
            if c == ".": # ignore cent amounts
                break
            if c.isnumeric():
                salary += c
        return int(salary) if salary else -1

    def validateEntry(self, name, salary, year, level):
        """
        Receives string name, integer salary, string year, string level
        Returns True if the entry is valid, else False
        An entry is valid if all the data is filled out, the player has a
        salary that is higher than the minimum and lower than the max,
        the year is correct, the player is in the MLB, and the player has
        not been counted already.
        """
        if not (name and salary != -1 and year and level): # make sure all fields are filled
            return False
        if name in self.salaries and salary == self.salaries[name]: # duplicate entry 
            return False
        if salary < self.minSalary or salary > self.maxSalary:
            return False
        if year != self.year: # data should be from current year
            return False
        if level != "MLB": # don't consider non MLB players
            return False
        return True

    def getOffer(self):
        """
        Returns a qualifying offer for a departing free agent player.
        This is equal to the average of the highest 125 salaries.
        """
        if not self.salaries:
            self.getSalaries()
        numSalaries = self.getSalaryList()
        return int(sum(numSalaries[:125]) / 125)

    def showInfo(self):
        """
        Prints minimum, average, maximum salary as well as qualifying offer
        value. Generates a graph of all given salaries.
        """
        if not self.salaries:
            self.getSalaries()
        numSalaries = self.getSalaryList()
        scaledVal = lambda n, minVal, maxVal : (n / numSalaries[0]) * \
               (maxVal - minVal) + minVal
        sizes = [scaledVal(n, 1, 100) for n in numSalaries[::-1]]
        colors = [scaledVal(n, 0, 1) for n in numSalaries[::-1]]
        plt.scatter(list(range(len(numSalaries))), numSalaries[::-1],
                sizes, c = colors, cmap = "turbo")
        plt.title("MLB Salaries")
        plt.ylabel("Salary ($)")
        plt.xlabel("Num lower paid players")
        plt.savefig("player_salaries.png")
        info = {"Minimum Salary": numSalaries[-1],
                "Average Salary": int(sum(numSalaries) / len(numSalaries)),
                "Maximum Salary": numSalaries[0],
                "Qualifying Offer Value": self.getOffer()}
        for msg in info:
            print(f"{msg}: ${info[msg]:,}")

    def getSalaryList(self):
        """
        Converts salary dictionary into list of salaries.
        Used for when player names are not needed.
        """
        numSalaries = list(self.salaries.values())
        numSalaries.sort(reverse = True)
        return numSalaries

def main():
    # min salary in 2010: 400,000
    # max reasonable salary: 50,000,000 (if a player is being paid more than
    # this, we should manually inspect this entry)
    offer = Offer(2016, 400000, 50000000, "https://questionnaire-148920.appspot.com/swe/data.html")
    offer.showInfo()

main()
