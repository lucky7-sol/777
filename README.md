# Lucky7 - Decentralized Lottery on Solana

A fair and transparent lottery system built on the Solana blockchain, featuring automated draws every 20 minutes and verifiable randomness.

## How It Works

### Token-Based Entry System
- **1 Raffle Entry = 10,000 $777 Tokens**
- More tokens = more entries = better odds
- Example: 50,000 tokens = 5 entries, 100,000 tokens = 10 entries

### Automated Draws
- Draws occur every 20 minutes automatically
- Winners are selected using Solana's Verifiable Random Function (VRF)
- Payouts are processed automatically to the winner's wallet

### Prize Pool
- 100% of the pool balance is awarded to winners
- All transactions are publicly viewable on the blockchain

## Features

### Real-time Dashboard
- **Prize Pool Display**: Live SOL balance from the prize wallet
- **Holder Count**: Number of active $777 token holders
- **Countdown Timer**: Time remaining until next draw
- **Winner History**: Previous winners and prize amounts

### Ticket Checker
- Enter any Solana wallet address to check ticket count
- Real-time token balance verification
- Automatic ticket calculation based on token holdings

### Transparency Tools
- **Public Wallet**: All funds held in publicly viewable wallet
- **Transaction History**: Every payout recorded on-chain
- **VRF Verification**: Cryptographically verifiable randomness

## Technical Implementation

### Smart Contract Architecture
- Built on Solana for fast, low-cost transactions
- Uses Solana's native VRF for provably fair randomness
- Automated execution without human intervention

### Winner Selection Process
1. **Snapshot Creation**: Take snapshot of all token holders
2. **Ticket Assignment**: Assign sequential ticket numbers based on holdings
3. **Random Selection**: VRF generates random number mapped to ticket range
4. **Winner Identification**: Find holder who owns the selected ticket number
5. **Automatic Payout**: Transfer prize directly to winner's wallet

### Frontend Technology
- Pure HTML/CSS/JavaScript implementation
- Real-time Solana RPC integration
- Responsive design for all devices
- No external dependencies beyond RPC endpoint

## Configuration

### Environment Variables
```javascript
const CONFIG = {
    RPC_ENDPOINT: 'https://mainnet.helius-rpc.com/?api-key=YOUR_KEY',
    WALLET_ADDRESS: 'G9wyu2uBqegt3Q6Q6qogX4Urk2Uo6A2XdkLCwH4tYebY',
    TOKEN_MINT: '8NQzZCy6YBHzzigczBoykLQzr3Q7EKdEYfjM94WJpump',
    TOKENS_PER_TICKET: 10000
};
```

### Key Parameters
- **Prize Wallet**: G9wyu2uBqegt3Q6Q6qogX4Urk2Uo6A2XdkLCwH4tYebY
- **Token Contract**: 8NQzZCy6YBHzzigczBoykLQzr3Q7EKdEYfjM94WJpump
- **Draw Frequency**: Every 20 minutes
- **Ticket Ratio**: 10,000 tokens per ticket

## File Structure

```
lucky7/
├── index.html          # Main application file
├── README.md          # This documentation
└── assets/            # Static assets (if any)
```

## Setup and Deployment

### Local Development
1. Clone the repository
2. Update RPC endpoint in CONFIG object
3. Open `index.html` in web browser
4. No build process required

### Production Deployment
1. Upload `index.html` to web server
2. Configure proper RPC endpoint with API key
3. Ensure HTTPS for wallet connections
4. Test all functionality before going live

## API Integration

### Solana RPC Methods Used
- `getBalance`: Prize pool balance
- `getProgramAccounts`: Token holder enumeration
- `getTokenAccountsByOwner`: Individual wallet ticket checking
- `getTokenSupply`: Fallback holder estimation

### Auto-refresh System
- Data updates every 30 seconds automatically
- Countdown timer updates every second
- Error handling for RPC failures

## Security Features

### Verifiable Randomness
- Uses Solana's cryptographic VRF
- Cannot be predicted or manipulated
- Publicly verifiable on-chain

### Transparency Measures
- All prize pool funds in public wallet
- Complete transaction history available
- Open-source frontend code
- Real-time monitoring capabilities

### Fair Play Guarantees
- Snapshot taken before random number generation
- Immutable record of all participants
- Deterministic winner selection process
- Independent verification possible

## Browser Compatibility

### Supported Browsers
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Required Features
- ES6 JavaScript support
- Fetch API
- CSS Grid and Flexbox
- Background blur effects

## Troubleshooting

### Common Issues
1. **RPC Errors**: Check API key and endpoint
2. **Slow Loading**: Try different RPC provider
3. **Wallet Not Found**: Verify wallet address format
4. **Display Issues**: Ensure modern browser support

### Error Handling
- Graceful degradation for RPC failures
- Alternative data sources for holder counts
- User-friendly error messages
- Automatic retry mechanisms

## Contributing

### Development Guidelines
- Maintain compatibility with existing wallet addresses
- Preserve draw timing synchronization
- Keep transparency features intact
- Test thoroughly before deployment

### Code Style
- Use modern JavaScript (ES6+)
- Maintain responsive design principles
- Follow existing naming conventions
- Include comprehensive error handling

## License

This project is open source. Please ensure compliance with local gambling and lottery regulations before deployment.

## Disclaimer

This is a lottery/gambling application. Users should be aware of the risks involved and gamble responsibly. The developers are not responsible for any financial losses. This system is provided as-is for educational and entertainment purposes.
