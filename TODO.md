
# Objective:
- If an existing user BOID token balance RAM is paid for by the boidcomtoken account:
  - release the RAM
  - require the user to provide RAM to pay for the token balance.

# Why does this need to be done?
- When a data entry is added to a contract table, someone has to pay for the extra RAM. This is typically the end-user or the contract owner. 
- In the case of BOID tokens, it is the contract owner (us). 
- costs BOID a lot of money to store currency info for every BOID token holder
    - due to the large amount of data 

# TODO
1. look over eosio.token contract

2. modify the contract so it will allow the RAM owner to be transferred from the boidcomtoken acct to the user (boidcomtoken holder)
