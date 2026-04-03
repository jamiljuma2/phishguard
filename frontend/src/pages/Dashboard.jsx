import React, { useState } from "react";
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';
import ReportModal from "../components/ReportModal";
import { useQuery } from '@tanstack/react-query';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { AlertTriangle, CheckCircle, Globe, Mail } from "lucide-react";
import PropTypes from "prop-types";
import api from "../api";
// Firebase removed

function Dashboard() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);
  const [allAlertsOpen, setAllAlertsOpen] = useState(false);
  // No user state needed

  // Use react-query for dashboard stats
  const { data: stats = {
    total_scans: 0,
    phishing_email: 0,
    phishing_sms: 0,
    phishing_url: 0,
    legitimate_email: 0,
    legitimate_sms: 0,
    legitimate_url: 0,
    recent: [],
  }, isLoading: loading, error } = useQuery({
    queryKey: ['dashboard_stats'],
    queryFn: async () => {
      const res = await api.get('/dashboard_stats');
      return res.data;
    },
    staleTime: 1000 * 60, // 1 minute
    retry: 1,
  });

  // Generate trend data for chart (last 7 scans by date)
  const trendData = React.useMemo(() => {
    if (!stats.recent) return [];
    return Array(7)
      .fill(0)
      .map((_, i) => {
        const d = new Date();
        d.setDate(d.getDate() - (6 - i));
        const day = d.toLocaleString("en-US", { weekday: "short" });
        const dayScans = stats.recent.filter((scan) => {
          const scanDate = new Date(scan.timestamp);
          return scanDate.toDateString() === d.toDateString();
        });
        return {
          name: day,
          phishing: dayScans.filter((s) => s.result === "Phishing").length,
          legitimate: dayScans.filter((s) => s.result === "Legitimate").length,
        };
      });
  }, [stats.recent]);



  if (error) {
    return (
      <div className="flex justify-center items-center h-full">
        <p className="text-red-500 dark:text-red-400">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-end gap-4 md:gap-0">
        <div>
          <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white">
            Threat Intelligence
          </h2>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            Real-time overview of your email security status.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="text-sm font-medium text-slate-500">
            Last 7 Days
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Scans"
          value={stats.total_scans}
          icon={<Mail className="text-blue-500" />}
          color="blue"
        />
        <StatsCard
          title="Phishing Emails"
          value={stats.phishing_email}
          icon={<AlertTriangle className="text-red-500" />}
          color="red"
        />
        <StatsCard
          title="Phishing SMS"
          value={stats.phishing_sms}
          icon={<AlertTriangle className="text-red-500" />}
          color="red"
        />
        <StatsCard
          title="Phishing URLs"
          value={stats.phishing_url}
          icon={<AlertTriangle className="text-red-500" />}
          color="red"
        />
        <StatsCard
          title="Legitimate Emails"
          value={stats.legitimate_email}
          icon={<CheckCircle className="text-emerald-500" />}
          color="emerald"
        />
        <StatsCard
          title="Legitimate SMS"
          value={stats.legitimate_sms}
          icon={<CheckCircle className="text-emerald-500" />}
          color="emerald"
        />
        <StatsCard
          title="Legitimate URLs"
          value={stats.legitimate_url}
          icon={<CheckCircle className="text-emerald-500" />}
          color="emerald"
        />
        <StatsCard
          title="Global Risk Level"
          value={
            stats.phishing_email + stats.phishing_sms + stats.phishing_url >
            stats.legitimate_email + stats.legitimate_sms + stats.legitimate_url
              ? "High"
              : "Low"
          }
          subtext={stats.total_scans > 0 ? "System Healthy" : "No Data"}
          icon={<Globe className="text-indigo-500" />}
          color="indigo"
        />
      </div>

      {/* Main Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 card bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-soft border border-slate-200 dark:border-slate-700 min-w-0">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-6">
            Detection Trends
          </h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={trendData}
                margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
              >
                <defs>
                  <linearGradient
                    id="colorPhishing"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="5%" stopColor="#EF4444" stopOpacity={0.1} />
                    <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorLegit" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.1} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis
                  dataKey="name"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#94a3b8" }}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#94a3b8" }}
                />
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#e2e8f0"
                />
                <Tooltip
                  contentStyle={{
                    borderRadius: "8px",
                    border: "none",
                    boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="phishing"
                  stroke="#EF4444"
                  fillOpacity={1}
                  fill="url(#colorPhishing)"
                />
                <Area
                  type="monotone"
                  dataKey="legitimate"
                  stroke="#10B981"
                  fillOpacity={1}
                  fill="url(#colorLegit)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-end mt-6">
            <button
              className="btn-primary px-6 py-2 text-sm"
              onClick={() => {
                setSelectedReport({
                  result: "Trend Report",
                  input_type: "summary",
                  input: `Detection trends over ${trendData.length} periods`,
                  confidence:
                    stats.total_scans > 0
                      ? (stats.phishing_email +
                          stats.phishing_sms +
                          stats.phishing_url) /
                        stats.total_scans
                      : 0,
                  total_scans: stats.total_scans,
                  phishing_total:
                    stats.phishing_email +
                    stats.phishing_sms +
                    stats.phishing_url,
                  legitimate_total:
                    stats.legitimate_email +
                    stats.legitimate_sms +
                    stats.legitimate_url,
                });
                setModalOpen(true);
              }}
            >
              View Full Report
            </button>
          </div>
        </div>

        <div className="card bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-soft border border-slate-200 dark:border-slate-700 min-w-0">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">
            Recent Alerts
          </h3>
          <div className="space-y-4">
            {(stats.recent || []).map((scan, i) => (
              <div
                key={scan.id || i}
                className="flex items-start gap-3 p-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors cursor-pointer"
              >
                <div
                  className={`mt-1 min-w-[8px] h-2 w-2 rounded-full ${scan.result === "Phishing" ? "bg-red-500" : "bg-emerald-500"}`}
                ></div>
                <div>
                  <p className="text-sm font-medium text-slate-800 dark:text-slate-200">
                    {scan.subject || scan.input || "No Subject"}
                  </p>
                  <p className="text-xs text-slate-500">
                    {scan.email || (scan.input_type === "sms" ? "SMS" : "URL")}
                  </p>
                </div>
                <button
                  className="btn-primary px-3 py-1 text-xs ml-4"
                  onClick={() => {
                    setSelectedReport(scan);
                    setModalOpen(true);
                  }}
                >
                  View Report
                </button>
              </div>
            ))}
          </div>
          <button
            className="w-full mt-6 py-2 text-sm text-accent hover:text-accent-hover font-medium border border-accent/20 rounded-lg hover:bg-accent/5 transition-colors"
            onClick={() => setAllAlertsOpen(true)}
          >
            View All Alerts
          </button>
          {allAlertsOpen && (
            <div
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
              role="dialog"
              aria-modal="true"
              aria-label="All Alerts"
              onClick={() => setAllAlertsOpen(false)}
              onKeyDown={(e) => {
                if (e.key === "Escape") setAllAlertsOpen(false);
              }}
            >
              <div
                className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-8 relative"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  className="absolute top-4 right-4 text-slate-400 hover:text-accent text-xl font-bold"
                  onClick={() => setAllAlertsOpen(false)}
                  aria-label="Close alerts"
                >
                  &times;
                </button>
                <h3 className="text-lg font-bold mb-4 text-slate-900 dark:text-white">
                  All Alerts
                </h3>
                <div className="space-y-3">
                  {stats.recent.length === 0 && (
                    <div className="text-slate-500">No alerts found.</div>
                  )}
                  {stats.recent.map((scan, i) => (
                    <div
                      key={scan.id || i}
                      className="flex items-start gap-3 p-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors cursor-pointer"
                    >
                      <div
                        className={`mt-1 min-w-[8px] h-2 w-2 rounded-full ${scan.result === "Phishing" ? "bg-red-500" : "bg-emerald-500"}`}
                      ></div>
                      <div>
                        <p className="text-sm font-medium text-slate-800 dark:text-slate-200">
                          {scan.subject || scan.input || "No Subject"}
                        </p>
                        <p className="text-xs text-slate-500">
                          {scan.email ||
                            (scan.input_type === "sms" ? "SMS" : "URL")}
                        </p>
                        <p className="text-xs text-slate-400 mt-1">
                          Type:{" "}
                          {scan.input_type
                            ? scan.input_type.charAt(0).toUpperCase() +
                              scan.input_type.slice(1)
                            : "Unknown"}
                        </p>
                        <p className="text-xs text-slate-400 mt-1">
                          Confidence:{" "}
                          {typeof scan.confidence === "number"
                            ? (scan.confidence * 100).toFixed(2) + "%"
                            : "N/A"}
                        </p>
                      </div>
                      <button
                        className="btn-primary px-3 py-1 text-xs ml-4"
                        onClick={() => {
                          setSelectedReport(scan);
                          setModalOpen(true);
                        }}
                      >
                        View Report
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <ReportModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        report={selectedReport}
      />
    </div>
  );
}

const colorMap = {
  blue: "bg-blue-50 dark:bg-blue-900/20",
  red: "bg-red-50 dark:bg-red-900/20",
  emerald: "bg-emerald-50 dark:bg-emerald-900/20",
  indigo: "bg-indigo-50 dark:bg-indigo-900/20",
};

function StatsCard({ title, value, icon, color, subtext }) {
  return (
    <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-soft border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
            {title}
          </p>
          <h3 className="text-3xl font-bold text-slate-900 dark:text-white mt-2">
            {value}
          </h3>
        </div>
        <div className={`p-3 rounded-xl ${colorMap[color] || colorMap.blue}`}>
          {icon}
        </div>
      </div>
      {subtext && (
        <div className="mt-4 flex items-center text-sm">
          <span className="text-slate-400 ml-2">{subtext}</span>
        </div>
      )}
    </div>
  );
}

StatsCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  icon: PropTypes.element.isRequired,
  color: PropTypes.string.isRequired,
  subtext: PropTypes.string,
};

export default Dashboard;
