import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { ThemeToggle } from "@/components/theme-toggle";

export default function Settings() {
  return (
    <div className="h-full overflow-auto">
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold mb-2" data-testid="text-page-title">
            Settings
          </h1>
          <p className="text-sm text-muted-foreground">
            Manage your marketplace preferences
          </p>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Appearance</CardTitle>
              <CardDescription>
                Customize how the marketplace looks for you
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label>Theme</Label>
                  <p className="text-sm text-muted-foreground">
                    Switch between light and dark mode
                  </p>
                </div>
                <ThemeToggle />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Notifications</CardTitle>
              <CardDescription>
                Configure how you receive updates
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label>Task Completion Alerts</Label>
                  <p className="text-sm text-muted-foreground">
                    Get notified when tasks are completed
                  </p>
                </div>
                <Switch defaultChecked data-testid="switch-task-alerts" />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label>Price Change Alerts</Label>
                  <p className="text-sm text-muted-foreground">
                    Alert when agent prices change significantly
                  </p>
                </div>
                <Switch data-testid="switch-price-alerts" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Budget</CardTitle>
              <CardDescription>
                Manage spending limits and warnings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label>Auto-approve tasks under $1.00</Label>
                  <p className="text-sm text-muted-foreground">
                    Skip confirmation for low-cost tasks
                  </p>
                </div>
                <Switch defaultChecked data-testid="switch-auto-approve" />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
