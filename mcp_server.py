# -*- coding: utf-8 -*-
"""
GenPark Agentic Commerce Sponsored Placement Router MCP Server
Exposes Sponsored Agent Placement (SAP) auction and algorithmic slotting tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GenParkAgenticCommerceSponsoredPlacementRouter

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-sponsored-placement-router", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "route_sponsored_agent_placement",
                        "description": "Optimizes in-context AI agent sponsored product placements (SAP) and algorithmic slotting yield.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt_intent_context": {
                                    "type": "object",
                                    "properties": {
                                        "user_prompt_summary": {"type": "string"},
                                        "extracted_intent_tags": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["extracted_intent_tags"]
                                },
                                "shortlist_slots_available": {"type": "integer"}
                            },
                            "required": ["prompt_intent_context"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "route_sponsored_agent_placement":
            router = GenParkAgenticCommerceSponsoredPlacementRouter()
            res = router.route_sponsored_agent_placement(
                prompt_intent_context=args.get("prompt_intent_context", {}),
                sponsor_bids=args.get("sponsor_bids"),
                shortlist_slots_available=args.get("shortlist_slots_available", 2)
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        r = GenParkAgenticCommerceSponsoredPlacementRouter()
        test_res = r.route_sponsored_agent_placement({"extracted_intent_tags": ["vacuum", "robot"]})
        print(f"Test Slot 1 Winner: {test_res['allocated_shortlist_winners'][0]['brand_name']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
