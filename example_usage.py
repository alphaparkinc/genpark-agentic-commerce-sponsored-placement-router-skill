# -*- coding: utf-8 -*-
"""
Example usage of GenParkAgenticCommerceSponsoredPlacementRouter
Demonstrates in-context algorithmic shortlisting auction for AI agents.
"""

from client import GenParkAgenticCommerceSponsoredPlacementRouter

def main():
    router = GenParkAgenticCommerceSponsoredPlacementRouter(reserve_cpc_usd=0.80)

    context = {
        "user_prompt_summary": "User wants autonomous robot vacuum recommendations with self-emptying dock",
        "extracted_intent_tags": ["vacuum", "robot", "smart home", "automatic empty"]
    }

    res = router.route_sponsored_agent_placement(context, shortlist_slots_available=2)

    print("================================================================")
    print("GenPark Agentic Commerce Sponsored Placement Router - Live Runs")
    print("================================================================\n")
    print(f"Prompt Context Intent   : {res['inferred_consumer_intent']}")
    print(f"Shortlist Slots Awarded : {res['total_slots_filled']}\n")
    print("Winning In-Context Placements:")
    for w in res["allocated_shortlist_winners"]:
        print(f"  [Slot #{w['shortlist_slot']}] {w['brand_name']:<18} | {w['sku_name']:<35} | Clearing CPC: ${w['clearing_cpc_usd']:.2f} (Bid: ${w['bid_cpc_usd']:.2f}, eCPM: ${w['expected_ecpm_usd']:.2f})")
    print("\nFull Bidder Leaderboard:")
    for b in res["full_auction_leaderboard"]:
        print(f"  * {b['brand_name']:<18} | RankScore: {b['rank_score']:>6.2f} | Bid: ${b['bid_cpc_usd']:.2f} | Relevance: {b['semantic_relevance']}")
    print()

if __name__ == "__main__":
    main()
