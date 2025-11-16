import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Download, Filter, Copy } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import { useToast } from "@/hooks/use-toast";
import type { BazaarBucksPayment, StripePayment } from "@shared/schema";

interface LocusPayment {
  id: string;
  timestamp: string;
  agent_id: string;
  agent_name: string;
  amount: number;
  memo: string;
  recipient_wallet: string;
  network: string;
  token: string;
}

export default function Payments() {
  const [activeTab, setActiveTab] = useState("locus");
  const { toast } = useToast();

  const { data: bazaarBucksPayments, isLoading: loadingBB, isError: errorBB, refetch: refetchBB } = useQuery<BazaarBucksPayment[]>({
    queryKey: ["/api/payments/bazaarbucks"],
  });

  const { data: stripePayments, isLoading: loadingStripe, isError: errorStripe, refetch: refetchStripe } = useQuery<StripePayment[]>({
    queryKey: ["/api/payments/stripe"],
  });

  const { data: locusPayments, isLoading: loadingLocus, isError: errorLocus, refetch: refetchLocus } = useQuery<LocusPayment[]>({
    queryKey: ["/api/payments/locus"],
  });

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied!",
      description: "Wallet address copied to clipboard",
    });
  };

  const handleExport = () => {
    const data = activeTab === "bazaarbucks" ? bazaarBucksPayments : stripePayments;
    const csv = convertToCSV(data || []);
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${activeTab}-payments-${new Date().toISOString().split("T")[0]}.csv`;
    a.click();
  };

  const convertToCSV = (data: any[]) => {
    if (data.length === 0) return "";
    const headers = Object.keys(data[0]).join(",");
    const rows = data.map((row) => Object.values(row).join(","));
    return [headers, ...rows].join("\n");
  };

  return (
    <div className="h-full overflow-auto">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-semibold mb-2" data-testid="text-page-title">
              Payment Logs
            </h1>
            <p className="text-sm text-muted-foreground">
              Track all internal and external transactions
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" data-testid="button-filter">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </Button>
            <Button onClick={handleExport} data-testid="button-export">
              <Download className="h-4 w-4 mr-2" />
              Export CSV
            </Button>
          </div>
        </div>

        <Card>
          <CardHeader className="p-6 pb-0">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="w-full justify-start">
                <TabsTrigger value="locus" data-testid="tab-locus">
                  Locus (Blockchain)
                </TabsTrigger>
                <TabsTrigger value="bazaarbucks" data-testid="tab-bazaarbucks">
                  BazaarBucks (Internal)
                </TabsTrigger>
                <TabsTrigger value="stripe" data-testid="tab-stripe">
                  Stripe (External)
                </TabsTrigger>
              </TabsList>

              <TabsContent value="locus" className="mt-6">
                <CardContent className="p-0">
                  {errorLocus ? (
                    <div className="text-center py-12">
                      <p className="text-destructive mb-4">Failed to load Locus payments</p>
                      <Button onClick={() => refetchLocus()} variant="outline" data-testid="button-retry-locus">
                        Retry
                      </Button>
                    </div>
                  ) : loadingLocus ? (
                    <div className="space-y-4 p-6">
                      {[...Array(5)].map((_, i) => (
                        <Skeleton key={i} className="h-14 w-full" />
                      ))}
                    </div>
                  ) : (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead className="text-xs uppercase">Time</TableHead>
                          <TableHead className="text-xs uppercase">Agent</TableHead>
                          <TableHead className="text-xs uppercase">Amount</TableHead>
                          <TableHead className="text-xs uppercase">Recipient</TableHead>
                          <TableHead className="text-xs uppercase">Network</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {locusPayments?.map((payment) => (
                          <TableRow key={payment.id} className="hover-elevate" data-testid={`row-locus-${payment.id}`}>
                            <TableCell className="font-mono text-sm">
                              {new Date(payment.timestamp).toLocaleString()}
                            </TableCell>
                            <TableCell data-testid={`text-locus-agent-${payment.id}`}>
                              {payment.agent_name}
                            </TableCell>
                            <TableCell className="font-mono font-medium" data-testid={`text-locus-amount-${payment.id}`}>
                              ${payment.amount.toFixed(2)} {payment.token}
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              <div className="flex items-center gap-2">
                                <span className="text-muted-foreground">
                                  {payment.recipient_wallet.slice(0, 6)}...{payment.recipient_wallet.slice(-4)}
                                </span>
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  className="h-6 w-6"
                                  onClick={() => copyToClipboard(payment.recipient_wallet)}
                                  data-testid={`button-copy-wallet-${payment.id}`}
                                >
                                  <Copy className="h-3 w-3" />
                                </Button>
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">{payment.network}</Badge>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}

                  {!loadingLocus && locusPayments?.length === 0 && (
                    <div className="text-center py-12">
                      <p className="text-muted-foreground">No Locus blockchain transactions yet</p>
                    </div>
                  )}
                </CardContent>
              </TabsContent>

              <TabsContent value="bazaarbucks" className="mt-6">
                <CardContent className="p-0">
                  {errorBB ? (
                    <div className="text-center py-12">
                      <p className="text-destructive mb-4">Failed to load BazaarBucks payments</p>
                      <Button onClick={() => refetchBB()} variant="outline" data-testid="button-retry-bb">
                        Retry
                      </Button>
                    </div>
                  ) : loadingBB ? (
                    <div className="space-y-4 p-6">
                      {[...Array(5)].map((_, i) => (
                        <Skeleton key={i} className="h-14 w-full" />
                      ))}
                    </div>
                  ) : (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead className="text-xs uppercase">Date</TableHead>
                          <TableHead className="text-xs uppercase">Agent</TableHead>
                          <TableHead className="text-xs uppercase">Type</TableHead>
                          <TableHead className="text-xs uppercase">Amount</TableHead>
                          <TableHead className="text-xs uppercase">Task ID</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {bazaarBucksPayments?.map((payment) => (
                          <TableRow key={payment.id} className="hover-elevate" data-testid={`row-payment-${payment.id}`}>
                            <TableCell className="font-mono text-sm">
                              {new Date(payment.createdAt).toLocaleDateString()}
                            </TableCell>
                            <TableCell data-testid={`text-agent-${payment.id}`}>{payment.agentId}</TableCell>
                            <TableCell>
                              <Badge variant="secondary">{payment.type}</Badge>
                            </TableCell>
                            <TableCell className="font-mono font-medium" data-testid={`text-amount-${payment.id}`}>
                              ${payment.amount.toFixed(2)}
                            </TableCell>
                            <TableCell className="font-mono text-xs text-muted-foreground">
                              {payment.taskId}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}

                  {!loadingBB && bazaarBucksPayments?.length === 0 && (
                    <div className="text-center py-12">
                      <p className="text-muted-foreground">No BazaarBucks transactions yet</p>
                    </div>
                  )}
                </CardContent>
              </TabsContent>

              <TabsContent value="stripe" className="mt-6">
                <CardContent className="p-0">
                  {errorStripe ? (
                    <div className="text-center py-12">
                      <p className="text-destructive mb-4">Failed to load Stripe payments</p>
                      <Button onClick={() => refetchStripe()} variant="outline" data-testid="button-retry-stripe">
                        Retry
                      </Button>
                    </div>
                  ) : loadingStripe ? (
                    <div className="space-y-4 p-6">
                      {[...Array(5)].map((_, i) => (
                        <Skeleton key={i} className="h-14 w-full" />
                      ))}
                    </div>
                  ) : (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead className="text-xs uppercase">Date</TableHead>
                          <TableHead className="text-xs uppercase">Vendor</TableHead>
                          <TableHead className="text-xs uppercase">Type</TableHead>
                          <TableHead className="text-xs uppercase">Amount</TableHead>
                          <TableHead className="text-xs uppercase">Status</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {stripePayments?.map((payment) => (
                          <TableRow key={payment.id} className="hover-elevate" data-testid={`row-stripe-${payment.id}`}>
                            <TableCell className="font-mono text-sm">
                              {new Date(payment.createdAt).toLocaleDateString()}
                            </TableCell>
                            <TableCell data-testid={`text-vendor-${payment.id}`}>{payment.vendor}</TableCell>
                            <TableCell>
                              <Badge variant="secondary">{payment.type}</Badge>
                            </TableCell>
                            <TableCell className="font-mono font-medium" data-testid={`text-stripe-amount-${payment.id}`}>
                              ${payment.amount.toFixed(2)}
                            </TableCell>
                            <TableCell>
                              <Badge
                                className={
                                  payment.status === "completed"
                                    ? "bg-status-online"
                                    : payment.status === "failed"
                                    ? "bg-destructive"
                                    : "bg-status-away"
                                }
                              >
                                {payment.status}
                              </Badge>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}

                  {!loadingStripe && stripePayments?.length === 0 && (
                    <div className="text-center py-12">
                      <p className="text-muted-foreground">No Stripe transactions yet</p>
                    </div>
                  )}
                </CardContent>
              </TabsContent>
            </Tabs>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}
