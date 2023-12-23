import requests

def get_delegators(validator_address):
    # Fetch the list of delegators from your specified Cosmos LCD endpoint
    response = requests.get(f'https://https://lcd.injective.network/cosmos/staking/v1beta1/validators/injvaloper....../delegations?pagination.limit=10000')
    if response.status_code == 200:
        return response.json()['delegation_responses']
    else:
        print("Error fetching delegators:", response.status_code)
        return None

def calculate_refund_amount(stake, conversion_factor):
    # Convert the stake from the smallest unit to the standard unit (INJ)
    standard_unit_stake = stake / conversion_factor
    # Calculate Standard 0.01% of the stake in standard units
    # return standard_unit_stake * 0.0001
    # Calculate peggo refund amount
    return standard_unit_stake * 0.001

def create_and_send_transactions(delegators, conversion_factor):
    total_refund = 0
    total_delegators = 0
    for delegator in delegators:
        stake = int(delegator['balance']['amount'])  # Extract the staked amount in smallest unit

        # Skip the delegator if the stake is zero
        if stake == 0:
            continue

        delegator_address = delegator['delegation']['delegator_address']  # Extract the delegator's address
        refund_amount = calculate_refund_amount(stake, conversion_factor)

        print("Delegator address: " + delegator_address)
        print("Stake in INJ: {:.10f}".format(stake / conversion_factor))
        print("Refund in INJ: {:.10f}".format(refund_amount))

        total_delegators += 1
        total_refund += refund_amount

        # TODO
        # Code to create and send transaction
        # Implement transaction creation, signing, and broadcasting here

    return total_refund, total_delegators

# Example usage
validator_address = 'injvaloper1......'
conversion_factor = 10**18  # Conversion factor from smallest unit to INJ
delegators = get_delegators(validator_address)

if delegators:
    total_refund, total_delegators  = create_and_send_transactions(delegators, conversion_factor)
    print(f"Total refund amount in INJ: {total_refund}")
    print(f"Total delegators: {total_delegators}")
else:
    print("Failed to retrieve delegators")
