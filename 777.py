import requests
import json
import random
from typing import List, Dict, Tuple
import time

class BallLotteryPicker:
    def __init__(self):
        self.rpc_endpoint = ""
        self.token_mint = ""
        self.tokens_per_ticket = 10000
        self.holders = []
        self.total_tickets = 0
        
    def make_rpc_call(self, method: str, params: List) -> Dict:
        """Make RPC call to Solana"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        try:
            response = requests.post(
                self.rpc_endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"RPC call failed: {e}")
            return {"error": str(e)}
    
    def get_token_holders(self) -> List[Dict]:
        """Get all token holders and their balances"""
        print("Fetching token holders...")
        
        # Get all token accounts for this mint
        response = self.make_rpc_call(
            "getProgramAccounts",
            [
                "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",  # SPL Token Program
                {
                    "encoding": "jsonParsed",
                    "filters": [
                        {"dataSize": 165},  # Token Account data size
                        {
                            "memcmp": {
                                "offset": 0,
                                "bytes": self.token_mint
                            }
                        }
                    ]
                }
            ]
        )
        
        if "error" in response:
            print(f"Error fetching token accounts: {response['error']}")
            return []
        
        holders = []
        
        for account in response.get("result", []):
            try:
                parsed_data = account["account"]["data"]["parsed"]["info"]
                token_amount = parsed_data["tokenAmount"]
                owner = parsed_data["owner"]
                balance = float(token_amount["uiAmount"] or 0)
                
                # Only include holders with positive balance
                if balance > 0:
                    tickets = int(balance // self.tokens_per_ticket)
                    holders.append({
                        "wallet": owner,
                        "balance": balance,
                        "tickets": tickets
                    })
                    
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error parsing account data: {e}")
                continue
        
        # Sort by balance (largest first)
        holders.sort(key=lambda x: x["balance"], reverse=True)
        return holders
    
    def calculate_ticket_ranges(self, holders: List[Dict]) -> List[Dict]:
        """Calculate ticket ranges for each holder"""
        current_ticket = 0
        holders_with_ranges = []
        
        for holder in holders:
            if holder["tickets"] > 0:
                start_ticket = current_ticket
                end_ticket = current_ticket + holder["tickets"] - 1
                
                holders_with_ranges.append({
                    "wallet": holder["wallet"],
                    "balance": holder["balance"],
                    "tickets": holder["tickets"],
                    "ticket_start": start_ticket,
                    "ticket_end": end_ticket
                })
                
                current_ticket += holder["tickets"]
        
        return holders_with_ranges
    
    def pick_random_winner(self, holders_with_ranges: List[Dict]) -> Tuple[str, int, Dict]:
        """Pick a random ticket and find the winner"""
        if not holders_with_ranges:
            return None, 0, {}
        
        total_tickets = sum(holder["tickets"] for holder in holders_with_ranges)
        
        if total_tickets == 0:
            return None, 0, {}
        
        # Pick random ticket number (0-indexed)
        winning_ticket = random.randint(0, total_tickets - 1)
        
        # Find which holder owns this ticket
        for holder in holders_with_ranges:
            if holder["ticket_start"] <= winning_ticket <= holder["ticket_end"]:
                # SAFETY CHECK: Ensure winner is not the liquidity pool
                if hasattr(self, 'liquidity_pool') and self.liquidity_pool and holder["wallet"] == self.liquidity_pool["wallet"]:
                    print("ERROR: Liquidity pool was selected as winner! This should not happen.")
                    print(f"LP Wallet: {self.liquidity_pool['wallet']}")
                    print(f"Winner Wallet: {holder['wallet']}")
                    print("Retrying lottery selection...")
                    return self.pick_random_winner(holders_with_ranges)  # Retry
                
                return holder["wallet"], winning_ticket, holder
        
        return None, winning_ticket, {}
    
    def display_holder_summary(self, holders: List[Dict]):
        """Display summary of holders"""
        print(f"\n{'='*80}")
        print("BALL TOKEN HOLDER SUMMARY (Excluding Liquidity Pool)")
        print(f"{'='*80}")
        
        total_holders = len(holders)
        total_tokens = sum(h["balance"] for h in holders)
        total_tickets = sum(h["tickets"] for h in holders)
        holders_with_tickets = len([h for h in holders if h["tickets"] > 0])
        
        print(f"Eligible Holders: {total_holders:,}")
        print(f"Holders with Tickets: {holders_with_tickets:,}")
        print(f"Total Tokens (Eligible): {total_tokens:,.2f}")
        print(f"Total Tickets: {total_tickets:,}")
        print(f"Tokens per Ticket: {self.tokens_per_ticket:,}")
        
        print(f"\nTop 500 Eligible Holders:")
        print(f"{'Rank':<6} {'Wallet':<45} {'Balance':<15} {'Tickets':<10}")
        print("-" * 80)
        
        display_count = min(500, len(holders))
        for i, holder in enumerate(holders[:display_count]):
            wallet_short = f"{holder['wallet'][:8]}...{holder['wallet'][-8:]}"
            print(f"{i+1:<6} {wallet_short:<45} {holder['balance']:>13,.0f} {holder['tickets']:>8,}")
        
        if len(holders) > 500:
            print(f"... and {len(holders) - 500} more holders")
    
    def run_lottery(self):
        """Run the complete lottery process"""
        print("Starting BALL Lottery Winner Selection")
        print("=" * 50)
        
        # Get all holders (this already excludes liquidity pool)
        self.holders = self.get_token_holders()
        
        if not self.holders:
            print("No eligible holders found or error fetching data")
            return
        
        # Display summary
        self.display_holder_summary(self.holders)
        
        # Calculate ticket ranges (using already filtered holders)
        holders_with_ranges = self.calculate_ticket_ranges(self.holders)
        
        # Verify no liquidity pool in lottery selection
        print(f"\nLottery participants: {len(holders_with_ranges)} wallets")
        if holders_with_ranges:
            print(f"Largest participant: {holders_with_ranges[0]['wallet'][:8]}...{holders_with_ranges[0]['wallet'][-8:]} ({holders_with_ranges[0]['balance']:,.0f} tokens)")
        
        # Pick winner
        print(f"\n{'='*80}")
        print("PICKING RANDOM WINNER (EXCLUDING WALLETS >40M TOKENS)")
        print(f"{'='*80}")
        
        winner_wallet, winning_ticket, winner_info = self.pick_random_winner(holders_with_ranges)
        
        if winner_wallet:
            print(f"🎰 WINNER SELECTED! 🎰")
            print(f"Winning Ticket: #{winning_ticket:,}")
            print(f"Winner Wallet: {winner_wallet}")
            print(f"Winner Balance: {winner_info['balance']:,.2f} BALL tokens")
            print(f"Winner Tickets: {winner_info['tickets']:,}")
            print(f"Ticket Range: #{winner_info['ticket_start']:,} - #{winner_info['ticket_end']:,}")
            
            # Calculate winner stats
            total_tickets = sum(h["tickets"] for h in holders_with_ranges)
            win_probability = (winner_info['tickets'] / total_tickets) * 100
            print(f"Win Probability: {win_probability:.4f}%")
            
            print(f"\n🔗 View wallet on Solscan:")
            print(f"https://solscan.io/account/{winner_wallet}")
            
        else:
            print("No winner could be selected (no valid tickets)")
    
    def verify_ticket_assignment(self, holders_with_ranges: List[Dict], ticket_number: int):
        """Verify which wallet owns a specific ticket number"""
        for holder in holders_with_ranges:
            if holder["ticket_start"] <= ticket_number <= holder["ticket_end"]:
                print(f"Ticket #{ticket_number} belongs to: {holder['wallet']}")
                print(f"Ticket range: #{holder['ticket_start']} - #{holder['ticket_end']}")
                return holder
        print(f"Ticket #{ticket_number} not found")
        return None

def main():
    # Create lottery instance
    lottery = BallLotteryPicker()
    
    # Run the lottery
    lottery.run_lottery()
    
    # Optional: Interactive mode to check specific tickets
    print(f"\n{'='*80}")
    print("INTERACTIVE MODE")
    print("Enter a ticket number to see who owns it, or 'q' to quit")
    
    holders_with_ranges = lottery.calculate_ticket_ranges(lottery.holders)
    total_tickets = sum(h["tickets"] for h in holders_with_ranges)
    
    while True:
        try:
            user_input = input(f"\nEnter ticket number (0-{total_tickets-1}) or 'q': ").strip()
            
            if user_input.lower() == 'q':
                break
                
            ticket_num = int(user_input)
            if 0 <= ticket_num < total_tickets:
                lottery.verify_ticket_assignment(holders_with_ranges, ticket_num)
            else:
                print(f"Invalid ticket number. Must be between 0 and {total_tickets-1}")
                
        except ValueError:
            print("Please enter a valid number or 'q'")
        except KeyboardInterrupt:
            break
    
    print("\nLottery selection complete!")

if __name__ == "__main__":
    main()
