# Qualifying Offer Calculator
Script to Analyze MLB salary data to find a free agent qualifying offer contract.
## Running
After downloading the project, navigate into the directory where it is stored.  Run

    pip install -r requirements.txt
To install the needed packages.
Alternatively, the requirements are listed here:

      0 beautifulsoup4==4.11.1
      1 certifi==2022.9.24
      2 charset-normalizer==2.1.1
      3 contourpy==1.0.5
      4 cycler==0.11.0
      5 fonttools==4.37.4
      6 idna==3.4
      7 kiwisolver==1.4.4
      8 matplotlib==3.6.0
      9 numpy==1.23.3
     10 packaging==21.3
     11 pyparsing==3.0.9
     12 python-dateutil==2.8.2
     13 requests==2.28.1
     14 six==1.16.0
     15 soupsieve==2.3.2.post1
     16 urllib3==1.26.12
After installing the package, run `python3 main.py`
## Output
This script will find the minimum, average, and maximum salary from the MLB data set.  It will also graph all of the MLB salaries, which will be output in player_salaries.png.
## Example Output
Minimum Salary: $507,500  
Average Salary: $3,339,282  
Maximum Salary: $34,571,429  
Qualifying Offer Value: $16,570,194  
![player_salaries](https://user-images.githubusercontent.com/94880155/193928192-1559edb9-3270-4823-b8ad-4645bfde0184.png)
## Possible Extensions
This project was set up to collect information about errors by collecting the names of players who did not pass the data validation.  From here, this could also be easily edited to track more information about why the player failed the validation to make debugging more simple.

# Question 1

The first inefficiency with this solution is that it uses unnecessary memory by creating string r.  This makes the solution require O(n) memory, where n is the length of s. An O(1) memory solution is possible (which I will describe momentarily).

Secondly, the second for loop should not be setting x to True during every iteration where s[x] == r[x], especially because x is the variable that is being incremented.  If one wanted to use this solution, they should check if s[x] != r[x] (and return False if so), and then return True at the conclusion of the loop.  If the loop finishes without returning False, we will know that the answer is True.

We can easily transform this solution into one that uses a constant amount of memory by using a while loop and simultaneously incrementing forwards and backward through the string.  For example, we could declare a variable l (left) = 0 and r (right) = len(s) - 1.  In each iteration, we will compare s[l] and s[r].  If they are not equal, we will know the string is not a palindrome so we can return False.  After this, we will increase l by 1 and subtract 1 from r.  We can repeat this process until l + 1 < r.

In addition to being more memory efficient, this will also only iterate over half the string.  However, this is a marginal gain as both solutions are O(n) time complexity.
