import logging
import time
from brownie import Wei, reverts

LOGGER = logging.getLogger(__name__)

def test_access_genome_provider(accounts, GenomeProviderPolygon):
    secret_hash = "0x00112233445566778899"
    provider = accounts[0].deploy(GenomeProviderPolygon, secret_hash)

    with reverts("Access denied"):
        provider.requestReveal(1, 2, 3, {'from':accounts[1]})

    with reverts("Access denied"):
        provider.setTraitConfig(1, [1], [0,1,2,3], [1,3,4,1], [5,2,1,1], {'from':accounts[1]})


def test_access(accounts, GenesisSale, roach_nft, reveal):
    stage1time = round(time.time()) - 1
    stage1duration = 60 * 60 * 24
    genesis_sale = accounts[0].deploy(GenesisSale, roach_nft, stage1time, stage1duration, 100, 10_000)

    with reverts("Access denied"):
        roach_nft.mint(accounts[0], "0x0", [0,0], 0, 0, {'from':accounts[1]})

    with reverts("Access denied"):
        roach_nft.mintGen0(accounts[0], 1, 0, "syndicate", {'from':accounts[1]})

    with reverts("Access denied"):
        roach_nft.setGenome(1, "0x0", {'from':accounts[1]})

    with reverts("Ownable: caller is not the owner"):
        roach_nft.setMetadataContract(roach_nft, {'from':accounts[1]})

    with reverts("Access denied"):
        genesis_sale.mintOperator(accounts[1], 5, 25, "syndicate", {'from':accounts[1]})

    with reverts("Ownable: caller is not the owner"):
        genesis_sale.setSigner(accounts[1], {'from':accounts[1]})

    with reverts("Ownable: caller is not the owner"):
        reveal.setSigner(accounts[1], {'from':accounts[1]})
