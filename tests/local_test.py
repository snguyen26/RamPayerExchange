import eosfactory.eosf as eosf
import sys
import os
import json
import argparse
import subprocess

RAM_PAYER_EXCHANGE_CONTRACT_PATH = \
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


assetDict = {'BOID': 0, 'EOS': 1}
getAssetQuantity = lambda x: float(x.split()[0])
getAssetType = lambda x: assetDict(x.split()[1])

# @param account  The account to set/delete a permission authority for
# @param permission  The permission name to set/delete an authority for
# @param authority  NULL, public key, JSON string, or filename defining the authority
# @param parent  The permission name of this parents permission (Defaults to "active")
def setAccountPermission(account, permission, authority, parent,
        json=False, code=False):
    if json: json = '--json'
    else: json = ''
    if code: code = '--add-code'
    else: code = ''
    permissionCmd =\
        'cleos set account permission {0} {1} {2} {3} -p {0}@active {4}'.format(
                        account, permission, authority, parent, json)
    subprocess.call(permissionCmd, shell=True)

# @param account  The account to set/delete a permission authority for
# @param contract  The account that owns the code for the action
# @param actionName  The type of the action
# @param permissionName  The permission name required for executing the given action 
def setActionPermission(
        account, contract, actionName, permissionName):
    permissionCmd = \
            'cleos set action permission {0} {1} {2} {3} -p {0}@active'.format(
                        account, contract, actionName, permissionName)
    subprocess.call(permissionCmd, shell=True)

def getBalance(x):
    if len(x.json['rows']) > 0:
        return float(x.json['rows'][0]['balance'].split()[0])
    else:
        return 0

transferPermission = lambda x,y:\
   '\'{{\
        "threshold": 1,\
        "keys": [\
            {{\
                "key" : "{0}",\
                "weight" : 1\
            }}\
        ],\
        "accounts": [\
            {{\
                "permission": {{"actor": "{1}", "permission": "eosio.code"}},\
                "weight" : 1\
            }}\
        ]\
    }}\''.format(x,y)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--build", action="store_true",
                        help="build new contract abis")
    args = parser.parse_args()

    # start single-node local testnet
    eosf.reset()

    # create master account from which
    # other account can be created
    # accessed via global variable: master
    eosf.create_master_account('master')

    # Create 7 accounts: eosio_token, eos, boid, acct1, acct2, acct3, acct4
    eosf.create_account(
        'eosio_token', master, account_name='eosio.token')
    eosf.create_account(
        'eos', master, account_name='eos')
    eosf.create_account(
        'boid', master, account_name='boid')
    eosf.create_account(
        'acct1', master, account_name='account1')
    eosf.create_account(
        'acct2', master, account_name='account2')
    eosf.create_account(
        'acct3', master, account_name='account3')
    eosf.create_account(
        'acct4', master, account_name='account4')

    # make build directory if it does not exist
    build_dir = os.path.join(RAM_PAYER_EXCHANGE_CONTRACT_PATH, 'build')
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

    # create reference to the token staking contract
    eosioToken_c = eosf.Contract(
        eosio_token, RAM_PAYER_EXCHANGE_CONTRACT_PATH)

    # build the token staking contract
    # if args.build:
    eosioToken_c.build()

    # deploy the token staking contract on the testnet
    eosioToken_c.deploy()

    # Set up master as issuer of EOS and boid as issuer of BOID
    # account.push_action(
    #		action_name,
    #		action_arguments_in_json,
    #		account_whose_permission_is_needed)
    eosioToken_c.push_action(
        'create',
        {
            'issuer': eos,
            'maximum_supply': '1000000000.0000 EOS'
        }, [eosio_token])

    eosioToken_c.push_action(
        'create',
        {
            'issuer': boid,
            'maximum_supply': '1000000000.0000 BOID'
        }, [eosio_token])

    # Distribute initial quantities of EOS & BOID
    eosioToken_c.push_action(
        'issue',
        {
            'to': acct1,
            'quantity': '1000.0000 EOS',
            'memo': 'memo'
        }, [eos])
    eosioToken_c.push_action(
        'issue',
        {
            'to': acct2,
            'quantity': '2000.0000 EOS',
            'memo': 'memo'
        }, [eos])
    
    eosioToken_c.push_action(
        'issue',
        {
            'to': boid,
            'quantity': '2000.0000 BOID',
            'memo': 'memo'
        }, [boid])

    # eosioToken_c.push_action(
    #     'issue',
    #     {
    #         'to': acct2,
    #         'quantity': '1000.0000 BOID',
    #         'memo': 'memo'
    #     }, [boid])

    print(eosioToken_c.table("accounts", boid))
    print(eosioToken_c.table("accounts", acct1))
    print(eosioToken_c.table("accounts", acct2))
    # print(eosioToken_c.table("accounts", acct3))

    boid.info()
    acct1.info()
    acct2.info()
    # acct3.info()

    # first transfer of boid 
    eosioToken_c.push_action(
        'transfer',
        {   
            'from': boid,
            'to': acct1,
            'quantity': '100.0000 BOID',
            'memo': 'memo'
        }, [boid,acct2])

    eosioToken_c.push_action(
        'transfer',
        {   
            'from': boid,
            'to': acct2,
            'quantity': '125.0000 BOID',
            'memo': 'memo'
        }, [boid,acct2])

    print(eosioToken_c.table("accounts", boid))
    print(eosioToken_c.table("accounts", acct1))
    print(eosioToken_c.table("accounts", acct2))

    boid.info()
    acct1.info()
    acct2.info()
    # acct3.info()

    # 2nd transfer of boid:
    eosioToken_c.push_action(
        'transfer',
        {   
            'from': boid,
            'to': acct1,
            'quantity': '150.0000 BOID',
            'memo': 'memo'
        }, [boid,acct1])

    eosioToken_c.push_action(
        'transfer',
        {   
            'from': boid,
            'to': acct2,
            'quantity': '200.0000 BOID',
            'memo': 'memo'
        }, [boid,acct2])

    print(eosioToken_c.table("accounts", boid))
    print(eosioToken_c.table("accounts", acct1))
    print(eosioToken_c.table("accounts", acct2))

    boid.info()
    acct1.info()
    acct2.info()

    # stop the testnet and exit python
    eosf.stop()
    sys.exit()
