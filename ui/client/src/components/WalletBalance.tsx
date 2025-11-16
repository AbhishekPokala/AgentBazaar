import { useQuery } from "@tanstack/react-query";
import { Wallet } from "lucide-react";
import { Card } from "@/components/ui/card";

interface WalletBalanceData {
  success: boolean;
  balance: number;
  wallet_address: string;
}

export function WalletBalance() {
  const { data, isLoading } = useQuery<WalletBalanceData>({
    queryKey: ["/api/wallet/balance"],
    refetchInterval: 30000,
  });

  if (isLoading) {
    return (
      <Card className="px-3 py-2" data-testid="card-wallet-loading">
        <div className="flex items-center gap-2">
          <Wallet className="h-4 w-4 text-muted-foreground" />
          <div className="text-sm text-muted-foreground">Loading...</div>
        </div>
      </Card>
    );
  }

  if (!data?.success) {
    return (
      <Card className="px-3 py-2" data-testid="card-wallet-error">
        <div className="flex items-center gap-2">
          <Wallet className="h-4 w-4 text-destructive" />
          <div className="text-sm text-destructive">Balance unavailable</div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="px-3 py-2" data-testid="card-wallet-balance">
      <div className="flex items-center gap-2">
        <Wallet className="h-4 w-4 text-primary" />
        <div className="flex items-baseline gap-1">
          <span className="text-sm font-mono font-semibold" data-testid="text-balance">
            {data.balance.toFixed(2)}
          </span>
          <span className="text-xs text-muted-foreground">USDC</span>
        </div>
      </div>
      <div className="text-xs text-muted-foreground mt-1">
        Base Network
      </div>
    </Card>
  );
}
