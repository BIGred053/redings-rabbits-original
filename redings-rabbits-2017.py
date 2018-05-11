import random
import math

## Original version of "Reding's Rabbits" Natural Selection Simulator built on repl.it by Evan McCullough (2016)
## Accessible and executable online at https://repl.it/@mr_mccullough/Redings-Rabbits-2017

num_alb=10 # The number of albino (recessive) alleles in the population. 10 is a default value to start.
num_brown=10  # The number of brown (dominant) alleles in the population. 10 is a default value to start.

# The simulation starts with a 50-50 breakdown of dominant and recessive alleles in the population.
pct_dom = 50
pct_rec = 50

brown_death = 25
alb_death = 75

round_count = 1
ans = "Y"
alb_ct=1
responded = False

# Variable to remember in which round the user decided to continue the simulation. Apparently needed to check if they want to continue again?
ans_round = 0

# Ask users to provide a population size, then figure out the total number of alleles (2 for every member of the population)
pop = int(input("Enter a starting population size: "))
num_alleles = pop * 2

# How frequently should results be output to show samples of the population over generations
interval = int(input("Print out results every _ rounds: "))

# At what rate do brown rabbits and albino rabbits die in this environment? The default values are 25% for brown and 75% for albino.
brown_death = int(input("Please enter a brown rabbit mortality rate (%): "))
alb_death = int(input("Please enter an albino rabbit mortality rate (%): "))

# Main body of the program. This will continue to run as long as the user wishes to continue and the potential for an albino rabbit remains in the population (at least 2 recessive alleles).
while(num_alb>=2 and ans.upper()=="Y"):
  

  # This is a reset so that the program will ask the user again if he/she wishes to continue every pop/10 rounds
  if(ans_round>0 and ((round_count-ans_round) == pop/10)):
    responded = False
  
  alleles = [] # Creates/empties our array of alleles each round
  rabbits = [] # Creates/empties our array of rabbits each round
  
  #Distribute allele frequency over population
  num_brown = round((num_alleles*pct_dom)/100)
  num_alb = round((num_alleles*pct_rec)/100)
  
  # Picking the larger number of alleles in order to reduce run time. Not sure if this actually saves any time.
  largest_num = max(num_brown, num_alb)
  
  # Generating list of all alleles in the population. Theoretically alternates until the min(num_alb, num_brown) is reached, then it will only add the allele that occurs at greater frequency.
  for i in range(0,largest_num):
    if(i<num_brown):
      alleles.append('B')
    if(i<num_alb):
      alleles.append('b')
    
  # Distribute alleles randomly into pairs to create our population of rabbits for each round  
  for i in range(0, pop):
    curr_rab = [alleles.pop(random.randint(0,len(alleles)-1)), alleles.pop(random.randint(0,len(alleles)-1))]
    rabbits.append(curr_rab)
  
  
  # Reset for each round to clear out any data on the last round's population
  albinos = []
  browns = []
  alb_kill_ct = 0
  brown_kill_ct = 0
  alb_ct = 0 
  brown_ct = 0 
  
  # Check each rabbit in our population to see how many are albino and how many are brown. Sort rabbits out according to this.
  for rabbit in rabbits:
    #print("Alleles: ", rabbit[0], rabbit[1])
    if(rabbit[0]=='b' and rabbit[1]=='b'):
      alb_ct+=1
      albinos.append(rabbit)
    else:
      brown_ct+=1
      browns.append(rabbit)
  
  # If it is the nth round, as defined by the user, print out a snapshot of this population
  #if(round_count%interval==0): 
  #  print("\nRound ", round_count, ":\n")
  #  print("Brown alleles- ", num_brown, " \nAlbino alleles- ", num_alb)
  #  print("Brown ct: ",len(browns), "Alb ct:", len(albinos))
  
  rec_tot = 0
  dom_tot = 0
  
  if(len(albinos)>1):
    alb_kill_ct = math.ceil(len(albinos)*(alb_death/100)) # Remove albinos from the population, according to their mortality rate
    for i in range(0, alb_kill_ct):
      #print("r", i, ";", alb_kill_ct)
      rabbits.remove(albinos.pop())  # Remove all killed albinos from our population of rabbits
  # elif was set up to automatically kill the only albino in the population, if only 1 existed. NOT redundant.
  elif(len(albinos)==1):
    alb_kill_ct=1
    rabbits.remove(albinos.pop()) 
        
        
  if(len(browns)>0):    
    brown_kill_ct = math.ceil(len(browns)*(brown_death/100))    
    for i in range(0, (brown_kill_ct)):
      rand_brown = random.choice(browns) # For each brown rabbit that dies, randomly choose that rabbit from our list of all browns
      rabbits.remove(rand_brown) # Remove chosen rabbit from overall population
      browns.remove(rand_brown) # Remove chosen rabbit from sub-population of browns, so that it isn't chosen again
      
  # Go back through to get allele counts, now that dead rabbits have been removed from the population
  for rabbit in rabbits:
      if(rabbit[0]=='b'):
        rec_tot+=1
      else:
        dom_tot+=1
      if(rabbit[1]=='b'):
        rec_tot+=1
      else:
        dom_tot+=1
  
  pct_dom = ((dom_tot)/(dom_tot+rec_tot))*100
  pct_rec = ((rec_tot)/(dom_tot+rec_tot))*100  
  
  if(round_count%interval==0 or rec_tot==0 or (alb_ct==0 and responded != True)):
    print("\nRound ", round_count, ":\n")
    print("Brown Rabbits: ", brown_ct, "\nAlbino Rabbits: ", alb_ct, "\n", alb_kill_ct, " albinos die.\n", brown_kill_ct, " brown rabbits die.\nRemaining rabbits: ", len(rabbits))
    print("Dom alleles: ", dom_tot, "\nRec Alleles: ", rec_tot)
    print("Dom percent: ", pct_dom, "\nRec Percent: ", pct_rec)
    
  round_count+=1
  
  if(alb_ct==0 and rec_tot>=2 and responded != True):
    ans = input("You are %d rounds in. There are no albino rabbits in the population, but there are enough alleles for another albino to theoretically be born. Run %d more rounds? (Y/N) " %(round_count-1, pop/10))
    ans_round= round_count-1
    responded = True
  
if(rec_tot<=1):  
  print("It took ", round_count-1, " rounds for all possibility for albino  rabbits to disappear.")  
  
