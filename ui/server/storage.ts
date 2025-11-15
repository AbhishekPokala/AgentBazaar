import {
  type Agent,
  type InsertAgent,
  type Task,
  type InsertTask,
  type TaskStep,
  type InsertTaskStep,
  type BazaarBucksPayment,
  type InsertBazaarBucksPayment,
  type StripePayment,
  type InsertStripePayment,
  type Message,
  type InsertMessage,
} from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  // Agents
  getAgents(): Promise<Agent[]>;
  getAgent(id: string): Promise<Agent | undefined>;
  
  // Tasks
  getTasks(): Promise<Task[]>;
  getTask(id: string): Promise<Task | undefined>;
  createTask(task: InsertTask): Promise<Task>;
  updateTask(id: string, updates: Partial<Task>): Promise<Task | undefined>;
  
  // Task Steps
  getTaskSteps(taskId: string): Promise<TaskStep[]>;
  createTaskStep(step: InsertTaskStep): Promise<TaskStep>;
  updateTaskStep(id: string, updates: Partial<TaskStep>): Promise<TaskStep | undefined>;
  
  // Payments
  getBazaarBucksPayments(): Promise<BazaarBucksPayment[]>;
  createBazaarBucksPayment(payment: InsertBazaarBucksPayment): Promise<BazaarBucksPayment>;
  
  getStripePayments(): Promise<StripePayment[]>;
  createStripePayment(payment: InsertStripePayment): Promise<StripePayment>;
  
  // Messages
  getMessages(): Promise<Message[]>;
  createMessage(message: InsertMessage): Promise<Message>;
}

export class MemStorage implements IStorage {
  private agents: Map<string, Agent>;
  private tasks: Map<string, Task>;
  private taskSteps: Map<string, TaskStep>;
  private bazaarBucksPayments: Map<string, BazaarBucksPayment>;
  private stripePayments: Map<string, StripePayment>;
  private messages: Map<string, Message>;

  constructor() {
    this.agents = new Map();
    this.tasks = new Map();
    this.taskSteps = new Map();
    this.bazaarBucksPayments = new Map();
    this.stripePayments = new Map();
    this.messages = new Map();
    this.seedData();
  }

  private seedData() {
    // Seed agents
    const mockAgents: Agent[] = [
      {
        id: "summarizer",
        name: "Summarizer Agent",
        description: "Condenses long text into concise summaries while preserving key information",
        skills: ["summarize", "extract", "condense"],
        basePrice: 0.10,
        dynamicPrice: 0.10,
        load: 2,
        rating: 4.8,
        jobsCompleted: 1247,
        endpointUrl: "http://summarizer:8001/execute",
        capabilities: [
          "Extract key points from articles and documents",
          "Create executive summaries",
          "Maintain context and tone in summaries",
          "Support multiple languages"
        ],
        avgResponseTime: 850,
        availability: true,
      },
      {
        id: "translator",
        name: "Translator Agent",
        description: "Professional translation across 50+ languages with context awareness",
        skills: ["translate", "localize", "language"],
        basePrice: 0.15,
        dynamicPrice: 0.18,
        load: 5,
        rating: 4.9,
        jobsCompleted: 2341,
        endpointUrl: "http://translator:8002/execute",
        capabilities: [
          "Translate text across 50+ languages",
          "Preserve technical terminology",
          "Context-aware translations",
          "Cultural localization"
        ],
        avgResponseTime: 920,
        availability: true,
      },
      {
        id: "sentiment",
        name: "Sentiment Analyzer",
        description: "Analyzes emotional tone and sentiment in text with detailed insights",
        skills: ["sentiment", "analyze", "emotion"],
        basePrice: 0.08,
        dynamicPrice: 0.08,
        load: 1,
        rating: 4.7,
        jobsCompleted: 856,
        endpointUrl: "http://sentiment:8003/execute",
        capabilities: [
          "Detect positive, negative, and neutral sentiment",
          "Identify emotional undertones",
          "Provide confidence scores",
          "Multi-language sentiment analysis"
        ],
        avgResponseTime: 640,
        availability: true,
      },
      {
        id: "formatter",
        name: "PDF Formatter",
        description: "Converts and formats documents with professional styling and layout",
        skills: ["format", "pdf", "document"],
        basePrice: 0.25,
        dynamicPrice: 0.32,
        load: 7,
        rating: 4.6,
        jobsCompleted: 423,
        endpointUrl: "http://formatter:8004/execute",
        capabilities: [
          "Convert to PDF with custom styling",
          "Apply professional templates",
          "Add headers, footers, and page numbers",
          "Integrate external font APIs"
        ],
        avgResponseTime: 1450,
        availability: true,
      },
      {
        id: "researcher",
        name: "Research Agent",
        description: "Gathers and synthesizes information from multiple sources",
        skills: ["research", "gather", "synthesize"],
        basePrice: 0.20,
        dynamicPrice: 0.20,
        load: 3,
        rating: 4.9,
        jobsCompleted: 678,
        endpointUrl: "http://researcher:8005/execute",
        capabilities: [
          "Multi-source information gathering",
          "Fact verification and citation",
          "Synthesize findings into reports",
          "Real-time data retrieval"
        ],
        avgResponseTime: 1850,
        availability: true,
      },
      {
        id: "coder",
        name: "Code Generator",
        description: "Generates production-ready code with best practices and documentation",
        skills: ["code", "generate", "program"],
        basePrice: 0.30,
        dynamicPrice: 0.39,
        load: 8,
        rating: 4.8,
        jobsCompleted: 1129,
        endpointUrl: "http://coder:8006/execute",
        capabilities: [
          "Generate code in 20+ languages",
          "Follow language-specific best practices",
          "Include comprehensive documentation",
          "Optimize for performance and readability"
        ],
        avgResponseTime: 1650,
        availability: true,
      },
    ];

    mockAgents.forEach(agent => this.agents.set(agent.id, agent));
  }

  // Agents
  async getAgents(): Promise<Agent[]> {
    return Array.from(this.agents.values());
  }

  async getAgent(id: string): Promise<Agent | undefined> {
    return this.agents.get(id);
  }

  // Tasks
  async getTasks(): Promise<Task[]> {
    return Array.from(this.tasks.values()).sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  async getTask(id: string): Promise<Task | undefined> {
    return this.tasks.get(id);
  }

  async createTask(insertTask: InsertTask): Promise<Task> {
    const id = randomUUID();
    const task: Task = {
      status: "created",
      maxBudget: 1.0,
      totalCost: 0,
      ...insertTask,
      id,
      createdAt: new Date(),
      completedAt: null,
    };
    this.tasks.set(id, task);
    return task;
  }

  async updateTask(id: string, updates: Partial<Task>): Promise<Task | undefined> {
    const task = this.tasks.get(id);
    if (!task) return undefined;
    
    const updated = { ...task, ...updates };
    this.tasks.set(id, updated);
    return updated;
  }

  // Task Steps
  async getTaskSteps(taskId: string): Promise<TaskStep[]> {
    return Array.from(this.taskSteps.values())
      .filter(step => step.taskId === taskId)
      .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
  }

  async createTaskStep(insertStep: InsertTaskStep): Promise<TaskStep> {
    const id = randomUUID();
    const step: TaskStep = {
      status: "pending",
      cost: 0,
      externalCost: 0,
      requiresExternalTool: false,
      result: null,
      executionTime: null,
      ...insertStep,
      id,
      createdAt: new Date(),
      completedAt: null,
    };
    this.taskSteps.set(id, step);
    return step;
  }

  async updateTaskStep(id: string, updates: Partial<TaskStep>): Promise<TaskStep | undefined> {
    const step = this.taskSteps.get(id);
    if (!step) return undefined;
    
    const updated = { ...step, ...updates };
    this.taskSteps.set(id, updated);
    return updated;
  }

  // Payments
  async getBazaarBucksPayments(): Promise<BazaarBucksPayment[]> {
    return Array.from(this.bazaarBucksPayments.values()).sort((a, b) =>
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  async createBazaarBucksPayment(insertPayment: InsertBazaarBucksPayment): Promise<BazaarBucksPayment> {
    const id = randomUUID();
    const payment: BazaarBucksPayment = {
      type: "agent_payment",
      ...insertPayment,
      id,
      createdAt: new Date(),
    };
    this.bazaarBucksPayments.set(id, payment);
    return payment;
  }

  async getStripePayments(): Promise<StripePayment[]> {
    return Array.from(this.stripePayments.values()).sort((a, b) =>
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  async createStripePayment(insertPayment: InsertStripePayment): Promise<StripePayment> {
    const id = randomUUID();
    const payment: StripePayment = {
      status: "completed",
      type: "card_spend",
      ...insertPayment,
      id,
      createdAt: new Date(),
    };
    this.stripePayments.set(id, payment);
    return payment;
  }

  // Messages
  async getMessages(): Promise<Message[]> {
    return Array.from(this.messages.values()).sort((a, b) =>
      new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
    );
  }

  async createMessage(insertMessage: InsertMessage): Promise<Message> {
    const id = randomUUID();
    const message: Message = {
      taskId: null,
      costBreakdown: null,
      ...insertMessage,
      id,
      createdAt: new Date(),
    };
    this.messages.set(id, message);
    return message;
  }
}

export const storage = new MemStorage();
