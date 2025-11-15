import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";

export async function registerRoutes(app: Express): Promise<Server> {
  // Get all agents
  app.get("/api/agents", async (_req, res) => {
    const agents = await storage.getAgents();
    res.json(agents);
  });

  // Get agent by ID
  app.get("/api/agents/:id", async (req, res) => {
    const agent = await storage.getAgent(req.params.id);
    if (!agent) {
      return res.status(404).json({ error: "Agent not found" });
    }
    res.json(agent);
  });

  // Get all tasks
  app.get("/api/tasks", async (_req, res) => {
    const tasks = await storage.getTasks();
    res.json(tasks);
  });

  // Get task by ID
  app.get("/api/tasks/:id", async (req, res) => {
    const task = await storage.getTask(req.params.id);
    if (!task) {
      return res.status(404).json({ error: "Task not found" });
    }
    res.json(task);
  });

  // Get task steps
  app.get("/api/tasks/:id/steps", async (req, res) => {
    const steps = await storage.getTaskSteps(req.params.id);
    res.json(steps);
  });

  // Create task
  app.post("/api/tasks", async (req, res) => {
    const task = await storage.createTask(req.body);
    res.json(task);
  });

  // Invoke agent (simulate execution)
  app.post("/api/invoke-agent", async (req, res) => {
    const { agentId, taskId, payload } = req.body;
    
    const agent = await storage.getAgent(agentId);
    if (!agent) {
      return res.status(404).json({ error: "Agent not found" });
    }

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 400));

    // Create mock result
    const result = {
      result: `Processed by ${agent.name}: ${JSON.stringify(payload).substring(0, 100)}...`,
      cost: agent.dynamicPrice,
      subtaskType: agent.skills[0],
      requiresExternalTool: agent.id === "formatter",
      externalCost: agent.id === "formatter" ? 0.05 : 0,
    };

    // Create task step
    const step = await storage.createTaskStep({
      taskId,
      agentId,
      subtaskType: result.subtaskType,
      status: "completed",
      cost: result.cost,
      externalCost: result.externalCost,
      requiresExternalTool: result.requiresExternalTool,
      result: result.result,
      executionTime: 800 + Math.floor(Math.random() * 400),
    });

    // Update step completion time
    await storage.updateTaskStep(step.id, {
      completedAt: new Date(),
    });

    // Create BazaarBucks payment
    await storage.createBazaarBucksPayment({
      taskId,
      agentId,
      amount: result.cost,
      type: "agent_payment",
    });

    // Create Stripe payment if external tool required
    if (result.requiresExternalTool) {
      await storage.createStripePayment({
        agentId,
        vendor: "Font API",
        amount: result.externalCost,
        status: "completed",
        type: "card_spend",
      });
    }

    res.json(result);
  });

  // Get BazaarBucks payments
  app.get("/api/payments/bazaarbucks", async (_req, res) => {
    const payments = await storage.getBazaarBucksPayments();
    res.json(payments);
  });

  // Get Stripe payments
  app.get("/api/payments/stripe", async (_req, res) => {
    const payments = await storage.getStripePayments();
    res.json(payments);
  });

  // Get messages
  app.get("/api/messages", async (_req, res) => {
    const messages = await storage.getMessages();
    res.json(messages);
  });

  // HubChat message (simulate orchestration)
  app.post("/api/hubchat/message", async (req, res) => {
    const { content } = req.body;

    // Create user message
    await storage.createMessage({
      role: "user",
      content,
      taskId: null,
      costBreakdown: null,
    });

    // Simulate HubChat thinking
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Mock orchestration logic
    const agents = await storage.getAgents();
    const selectedAgents = agents.slice(0, 2 + Math.floor(Math.random() * 2));

    const subtasks = selectedAgents.map(agent => ({
      agent: agent.name,
      cost: agent.dynamicPrice,
    }));

    const totalCost = subtasks.reduce((sum, st) => sum + st.cost, 0);

    // Create task
    const task = await storage.createTask({
      userQuery: content,
      requiredSkills: selectedAgents.flatMap(a => a.skills.slice(0, 1)),
      status: "created",
      maxBudget: 1.0,
      totalCost,
    });

    // Create response message
    const responseContent = `I'll help you with that. I've planned a ${selectedAgents.length}-step workflow using ${selectedAgents.map(a => a.name).join(", ")}. The estimated cost is $${totalCost.toFixed(2)} in BazaarBucks.`;

    await storage.createMessage({
      role: "assistant",
      content: responseContent,
      taskId: task.id,
      costBreakdown: { subtasks, total: totalCost },
    });

    // Execute workflow in background (simulate)
    selectedAgents.forEach(async (agent, idx) => {
      setTimeout(async () => {
        await storage.createTaskStep({
          taskId: task.id,
          agentId: agent.id,
          subtaskType: agent.skills[0],
          status: "completed",
          cost: agent.dynamicPrice,
          externalCost: 0,
          requiresExternalTool: false,
          result: `${agent.name} completed ${agent.skills[0]} successfully`,
          executionTime: 800 + Math.floor(Math.random() * 600),
        });

        await storage.createBazaarBucksPayment({
          taskId: task.id,
          agentId: agent.id,
          amount: agent.dynamicPrice,
          type: "agent_payment",
        });

        if (idx === selectedAgents.length - 1) {
          await storage.updateTask(task.id, {
            status: "completed",
            completedAt: new Date(),
          });
        }
      }, (idx + 1) * 1000);
    });

    res.json({ success: true });
  });

  const httpServer = createServer(app);
  return httpServer;
}
