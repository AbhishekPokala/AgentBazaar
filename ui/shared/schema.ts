import { sql } from "drizzle-orm";
import { pgTable, text, varchar, integer, real, timestamp, boolean, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// Agent Schema
export const agents = pgTable("agents", {
  id: varchar("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description").notNull(),
  skills: text("skills").array().notNull(),
  basePrice: real("base_price").notNull(),
  dynamicPrice: real("dynamic_price").notNull(),
  load: integer("load").notNull().default(0),
  rating: real("rating").notNull().default(5.0),
  jobsCompleted: integer("jobs_completed").notNull().default(0),
  endpointUrl: text("endpoint_url").notNull(),
  capabilities: text("capabilities").array().notNull(),
  avgResponseTime: integer("avg_response_time").notNull().default(1000), // ms
  availability: boolean("availability").notNull().default(true),
});

export const insertAgentSchema = createInsertSchema(agents);
export type InsertAgent = z.infer<typeof insertAgentSchema>;
export type Agent = typeof agents.$inferSelect;

// Task Schema
export const tasks = pgTable("tasks", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userQuery: text("user_query").notNull(),
  requiredSkills: text("required_skills").array().notNull(),
  status: text("status").notNull().default("created"), // created, in_progress, completed, failed
  maxBudget: real("max_budget").notNull().default(1.0),
  totalCost: real("total_cost").notNull().default(0),
  createdAt: timestamp("created_at").notNull().defaultNow(),
  completedAt: timestamp("completed_at"),
});

export const insertTaskSchema = createInsertSchema(tasks).omit({
  id: true,
  createdAt: true,
  completedAt: true,
});
export type InsertTask = z.infer<typeof insertTaskSchema>;
export type Task = typeof tasks.$inferSelect;

// Task Step Schema (for execution timeline)
export const taskSteps = pgTable("task_steps", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  taskId: varchar("task_id").notNull(),
  agentId: varchar("agent_id").notNull(),
  subtaskType: text("subtask_type").notNull(),
  status: text("status").notNull().default("pending"), // pending, in_progress, completed, failed
  cost: real("cost").notNull().default(0),
  externalCost: real("external_cost").notNull().default(0),
  requiresExternalTool: boolean("requires_external_tool").notNull().default(false),
  result: text("result"),
  executionTime: integer("execution_time"), // ms
  createdAt: timestamp("created_at").notNull().defaultNow(),
  completedAt: timestamp("completed_at"),
});

export const insertTaskStepSchema = createInsertSchema(taskSteps).omit({
  id: true,
  createdAt: true,
  completedAt: true,
});
export type InsertTaskStep = z.infer<typeof insertTaskStepSchema>;
export type TaskStep = typeof taskSteps.$inferSelect;

// Payment Schema (BazaarBucks - Internal)
export const bazaarBucksPayments = pgTable("bazaarbucks_payments", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  taskId: varchar("task_id").notNull(),
  agentId: varchar("agent_id").notNull(),
  amount: real("amount").notNull(),
  type: text("type").notNull().default("agent_payment"), // agent_payment, platform_fee, refund
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const insertBazaarBucksPaymentSchema = createInsertSchema(bazaarBucksPayments).omit({
  id: true,
  createdAt: true,
});
export type InsertBazaarBucksPayment = z.infer<typeof insertBazaarBucksPaymentSchema>;
export type BazaarBucksPayment = typeof bazaarBucksPayments.$inferSelect;

// Payment Schema (Stripe - External)
export const stripePayments = pgTable("stripe_payments", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  agentId: varchar("agent_id").notNull(),
  vendor: text("vendor").notNull(),
  amount: real("amount").notNull(),
  status: text("status").notNull().default("completed"), // pending, completed, failed
  type: text("type").notNull().default("card_spend"), // card_spend, balance_load
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const insertStripePaymentSchema = createInsertSchema(stripePayments).omit({
  id: true,
  createdAt: true,
});
export type InsertStripePayment = z.infer<typeof insertStripePaymentSchema>;
export type StripePayment = typeof stripePayments.$inferSelect;

// Message Schema (HubChat)
export const messages = pgTable("messages", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  role: text("role").notNull(), // user, assistant
  content: text("content").notNull(),
  taskId: varchar("task_id"),
  costBreakdown: jsonb("cost_breakdown"), // { subtasks: [{agent, cost}], total }
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const insertMessageSchema = createInsertSchema(messages).omit({
  id: true,
  createdAt: true,
});
export type InsertMessage = z.infer<typeof insertMessageSchema>;
export type Message = typeof messages.$inferSelect;
