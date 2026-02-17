import React, { useState } from "react";
import ReportModal from "../components/ReportModal";
import { Search, Filter, CheckCircle, AlertTriangle } from "lucide-react";
import api from "../api";
import { auth } from "../firebase";
import { onAuthStateChanged } from "firebase/auth";
import { useQuery } from '@tanstack/react-query';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

function History() {
  const [searchTerm, setSearchTerm] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);
  const [user, setUser] = useState(null);

  React.useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);

  // Use react-query for scan history
  const { data: historyData = [], isLoading: loading, error } = useQuery({
    queryKey: ['scan_history', user?.uid],
    queryFn: async () => {
      if (!user) throw new Error('Not authenticated');
      const res = await api.get('/history');
      return res.data;
    },
    enabled: !!user,
    staleTime: 1000 * 60, // 1 minute
    retry: 1,
  });

  const filteredData = historyData.filter(
    (item) =>
      (item.subject || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.email || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.input || "").toLowerCase().includes(searchTerm.toLowerCase()),
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white">
              <Skeleton width={180} />
            </h1>
            <p className="text-slate-500 dark:text-slate-400 mt-1">
              <Skeleton width={220} />
            </p>
          </div>
          <div className="flex gap-3 w-full md:w-auto">
            <div className="relative flex-grow md:flex-grow-0">
              <Skeleton width={220} height={40} />
            </div>
            <Skeleton width={90} height={40} />
          </div>
        </div>
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-soft border border-slate-200 dark:border-slate-700 overflow-hidden">
          <Skeleton height={300} />
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex flex-col justify-center items-center h-full text-center">
        <p className="text-xl font-medium text-slate-700 dark:text-white mb-4">
          Please sign in to view your scan history.
        </p>
        <button
          onClick={() => {
            /* Trigger login modal here if desired, or let Navbar handle it */ alert(
              "Sign in functionality is available via the navigation bar.",
            );
          }}
          className="btn-primary px-6 py-3"
        >
          Sign In / Sign Up
        </button>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-full">
        <p className="text-red-500 dark:text-red-400">Error: {error}</p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white">
              Scan History
            </h1>
            <p className="text-slate-500 dark:text-slate-400 mt-1">
              Review your past analysis reports.
            </p>
          </div>

          <div className="flex gap-3 w-full md:w-auto">
            <div className="relative flex-grow md:flex-grow-0">
              <Search
                className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400"
                size={20}
              />
              <input
                type="text"
                placeholder="Search history..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 w-full md:w-64 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-accent focus:border-transparent outline-none transition-all"
              />
            </div>
            <button className="flex items-center gap-2 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors">
              <Filter size={18} />
              <span>Filter</span>
            </button>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-soft border border-slate-200 dark:border-slate-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-700">
                  <th className="px-6 py-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Content / Sender
                  </th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Confidence
                  </th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-4 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider text-right">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                {filteredData.length > 0 ? (
                  filteredData.map((item) => (
                    <tr
                      key={item.id}
                      className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border ${
                            item.result === "Phishing"
                              ? "bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800"
                              : "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800"
                          }`}
                        >
                          {item.result === "Phishing" ? (
                            <AlertTriangle size={14} />
                          ) : (
                            <CheckCircle size={14} />
                          )}
                          {item.result}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-900 dark:text-white capitalize">
                        {item.input_type || "N/A"}
                      </td>
                      <td className="px-6 py-4">
                        <div>
                          <div className="text-sm font-medium text-slate-900 dark:text-white">
                            {item.input_type === "email"
                              ? item.subject
                              : (item.input?.substring(0, 50) || "N/A") +
                                ((item.input?.length || 0) > 50 ? "..." : "")}
                          </div>
                          <div className="text-xs text-slate-500 dark:text-slate-400">
                            {item.input_type === "email" ? item.email : ""}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${item.result === "Phishing" ? "bg-red-500" : "bg-emerald-500"}`}
                              style={{
                                width: `${Math.round(item.confidence * 100)}%`,
                              }} // Ensure confidence is a percentage
                            />
                          </div>
                          <span className="text-sm text-slate-600 dark:text-slate-300">
                            {Math.round(item.confidence * 100)}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-500 dark:text-slate-400">
                        {item.timestamp
                          ? new Date(item.timestamp).toLocaleDateString()
                          : ""}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          className="btn-primary px-4 py-1 text-xs"
                          onClick={() => {
                            setSelectedReport(item);
                            setModalOpen(true);
                          }}
                        >
                          View Report
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan="6"
                      className="px-6 py-4 text-center text-slate-500 dark:text-slate-400"
                    >
                      No scan history found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <ReportModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        report={selectedReport}
      />
    </>
  );
}

export default History;
