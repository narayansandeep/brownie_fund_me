from brownie import FundMe, MockV3Aggregator,network, config
from scripts.helpful_scripts import deploy_mock, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account=get_account()
    # now we need to pass the address of the price feed
    # if we are on a persistent address then pass the rinkeby address
    # Here we want to make the local ganache just as a dev env
    # since price feeds are not available for dev or local environments we need to do thi
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        # call function to deploy the mock
        deploy_mock()
       
        price_feed_address = MockV3Aggregator[-1].address
       
    # now deploy the actual contract
    fund_me = FundMe.deploy(

        price_feed_address,
        {"from":account},
        publish_source=config["networks"][network.show_active()].get("verify"))
    print(f'Contract deployed to {fund_me.address}')
    return fund_me

def main():
    deploy_fund_me()
    
    