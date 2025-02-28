// pages/dashboard.tsx
import { useEffect, useState } from "react";
import Head from "next/head";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface Metrics {
  queueSize: number;
  crawled: number;
  errors: number;
  performance: number;
  timestamp: number;
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics[]>([]);
  const errorThreshold = 5;
  const performanceThreshold = 50;

  useEffect(() => {
    // Connect to the WebSocket endpoint provided by the RealTimeMetricsPlugin.
    const ws = new WebSocket("ws://localhost:3001/ws/metrics");
    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (event) => {
      const data: Metrics = JSON.parse(event.data);
      setMetrics((prev) => [...prev, data]);
      if (data.errors > errorThreshold) {
        toast.error(`Error rate spiked to ${data.errors}%!`);
      }
      if (data.performance < performanceThreshold) {
        toast.warn(`Performance dipped to ${data.performance}%!`);
      }
    };
    ws.onerror = (err) => console.error("WebSocket error:", err);
    return () => ws.close();
  }, []);

  // Use the latest metrics for the cards.
  const latest =
    metrics.length > 0
      ? metrics[metrics.length - 1]
      : {
          queueSize: 0,
          crawled: 0,
          errors: 0,
          performance: 100,
          timestamp: Date.now(),
        };

  // Prepare data for a bar chart.
  const chartData = metrics.map((m) => ({
    time: new Date(m.timestamp).toLocaleTimeString(),
    "Queue Size": m.queueSize,
    Crawled: m.crawled,
    Errors: m.errors,
    Performance: m.performance,
  }));

  return (
    <>
      <Head>
        <title>Crawl Dashboard</title>
      </Head>
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">Crawl Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <Card>
            <CardHeader>
              <CardTitle>Queue Size</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-semibold">{latest.queueSize}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Crawled</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-semibold">{latest.crawled}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Errors</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-semibold">{latest.errors}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-semibold">{latest.performance}%</p>
            </CardContent>
          </Card>
        </div>
        <Separator className="my-6" />
        <div className="mb-6 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="Queue Size" fill="#3b82f6" />
              <Bar dataKey="Crawled" fill="#10b981" />
              <Bar dataKey="Errors" fill="#ef4444" />
              <Bar dataKey="Performance" fill="#f59e0b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <ToastContainer />
      </div>
    </>
  );
}
