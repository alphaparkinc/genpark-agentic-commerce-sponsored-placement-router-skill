# -*- coding: utf-8 -*-
"""
GenPark Agentic Commerce Sponsored Placement Router Client
Optimizes in-context AI agent sponsored product placements (SAP) and algorithmic slotting yield.
Zero external dependencies -- Python 3.9+ standard library only.
"""

import math
from typing import Dict, Any, List

class GenParkAgenticCommerceSponsoredPlacementRouter:
    """
    Sponsored Agent Placement (SAP) Yield Auctioneer:
    Replaces visual human banner ads with in-context algorithmic consideration slotting
    using Quality-weighted Generalized Second Price (Q-GSP) auctions and semantic intent scoring.
    """

    def __init__(self, reserve_cpc_usd: float = 0.50, relevance_exponent: float = 1.35):
        self.reserve_cpc = reserve_cpc_usd
        self.alpha = relevance_exponent

    def calculate_semantic_relevance(self, intent_tags: List[str], brand_tags: List[str]) -> float:
        """Jaccard-cosine overlap between user intent context and brand catalog metadata."""
        set_i = set(t.lower() for t in intent_tags)
        set_b = set(t.lower() for t in brand_tags)
        if not set_i or not set_b:
            return 0.5
        intersection = len(set_i.intersection(set_b))
        union = len(set_i.union(set_b))
        return round(intersection / union, 3)

    def route_sponsored_agent_placement(
        self,
        prompt_intent_context: Dict[str, Any],
        sponsor_bids: List[Dict[str, Any]] = None,
        shortlist_slots_available: int = 2
    ) -> Dict[str, Any]:
        """
        Executes real-time Q-GSP auction to select sponsored SKUs injected into AI agent shortlist.
        """
        if sponsor_bids is None:
            sponsor_bids = [
                {
                    "campaign_id": "SAP-DYSON-01",
                    "brand_name": "Dyson Official",
                    "sku_name": "Dyson V15 Detect Cordless Vacuum",
                    "bid_cpc_usd": 3.80,
                    "historical_agent_cvr": 0.082,
                    "historical_shortlist_ctr": 0.145,
                    "tags": ["vacuum", "cordless", "pet hair", "smart home", "premium"]
                },
                {
                    "campaign_id": "SAP-ROBOROCK-02",
                    "brand_name": "Roborock",
                    "sku_name": "Roborock S8 Pro Ultra Robot Vacuum",
                    "bid_cpc_usd": 4.50,
                    "historical_agent_cvr": 0.095,
                    "historical_shortlist_ctr": 0.160,
                    "tags": ["vacuum", "robot", "smart home", "automatic empty", "mop"]
                },
                {
                    "campaign_id": "SAP-SHARK-03",
                    "brand_name": "Shark Clean",
                    "sku_name": "Shark Stratos Upright Vacuum",
                    "bid_cpc_usd": 2.20,
                    "historical_agent_cvr": 0.068,
                    "historical_shortlist_ctr": 0.110,
                    "tags": ["vacuum", "upright", "budget friendly", "pet hair"]
                },
                {
                    "campaign_id": "SAP-ROOMBA-04",
                    "brand_name": "iRobot Roomba",
                    "sku_name": "Roomba Combo j9+",
                    "bid_cpc_usd": 3.10,
                    "historical_agent_cvr": 0.075,
                    "historical_shortlist_ctr": 0.125,
                    "tags": ["vacuum", "robot", "smart home", "pet obstacle avoidance"]
                }
            ]

        intent_tags = prompt_intent_context.get("extracted_intent_tags", ["vacuum", "robot", "smart home"])

        ranked_bidders = []
        for bid in sponsor_bids:
            relevance = self.calculate_semantic_relevance(intent_tags, bid.get("tags", []))
            # Relevance weighting
            effective_relevance = max(0.1, relevance ** self.alpha)

            cvr = bid.get("historical_agent_cvr", 0.05)
            ctr = bid.get("historical_shortlist_ctr", 0.10)
            cpc_bid = bid.get("bid_cpc_usd", 1.0)

            # Quality Score Q = CTR * CVR * (Relevance ^ alpha)
            quality_factor = ctr * cvr * effective_relevance
            rank_score = cpc_bid * quality_factor * 1000.0

            expected_ecpm = 1000.0 * ctr * cpc_bid * effective_relevance

            ranked_bidders.append({
                "campaign_id": bid["campaign_id"],
                "brand_name": bid["brand_name"],
                "sku_name": bid["sku_name"],
                "bid_cpc_usd": cpc_bid,
                "semantic_relevance": relevance,
                "rank_score": round(rank_score, 2),
                "expected_ecpm_usd": round(expected_ecpm, 2),
                "quality_factor": round(quality_factor, 6)
            })

        # Rank descending by rank score
        ranked_bidders.sort(key=lambda x: x["rank_score"], reverse=True)

        # Q-GSP Clearing Price calculation for top winners
        winners = []
        for i in range(min(shortlist_slots_available, len(ranked_bidders))):
            curr = ranked_bidders[i]
            runner_up = ranked_bidders[i + 1] if i + 1 < len(ranked_bidders) else None

            if runner_up and curr["quality_factor"] > 0:
                clearing_cpc = max(self.reserve_cpc, round((runner_up["rank_score"] / (curr["quality_factor"] * 1000.0)), 2))
            else:
                clearing_cpc = self.reserve_cpc

            winners.append({
                "shortlist_slot": i + 1,
                "campaign_id": curr["campaign_id"],
                "brand_name": curr["brand_name"],
                "sku_name": curr["sku_name"],
                "clearing_cpc_usd": clearing_cpc,
                "bid_cpc_usd": curr["bid_cpc_usd"],
                "semantic_relevance": curr["semantic_relevance"],
                "expected_ecpm_usd": curr["expected_ecpm_usd"]
            })

        return {
            "inferred_consumer_intent": prompt_intent_context.get("user_prompt_summary", "Autonomous robotic vacuum recommendation"),
            "allocated_shortlist_winners": winners,
            "total_slots_filled": len(winners),
            "reserve_cpc_usd": self.reserve_cpc,
            "full_auction_leaderboard": ranked_bidders
        }
