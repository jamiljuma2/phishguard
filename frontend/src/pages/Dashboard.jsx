import React, { useEffect, useState } from 'react';
import ReportModal from '../components/ReportModal';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertTriangle, CheckCircle, Globe, Mail } from 'lucide-react';
import PropTypes from 'prop-types';
import api from '../api';

function Dashboard() {
    const [modalOpen, setModalOpen] = useState(false);
    const [selectedReport, setSelectedReport] = useState(null);
    const [stats, setStats] = useState({
        total_scans: 0,
        phishing_email: 0,
        phishing_sms: 0,
        phishing_url: 0,
        legitimate_email: 0,
        legitimate_sms: 0,
        legitimate_url: 0,
        recent: []
    });
    const [trendData, setTrendData] = useState([]);
    useEffect(() => {
        api.get('/dashboard_stats').then(res => {
            setStats(res.data);
            // Generate trend data for chart (last 7 scans by date)
            const trend = Array(7).fill(0).map((_, i) => {
                const d = new Date();
                d.setDate(d.getDate() - (6 - i));
                const day = d.toLocaleString('en-US', { weekday: 'short' });
                const dayScans = res.data.recent.filter(scan => {
                    const scanDate = new Date(scan.timestamp);
                    return scanDate.toDateString() === d.toDateString();
                });
                return {
                    name: day,
                    phishing: dayScans.filter(s => s.result === 'Phishing').length,
                    legitimate: dayScans.filter(s => s.result === 'Legitimate').length,
                };
            });
            setTrendData(trend);
        });
    }, []);

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row justify-between items-end">
                <div>
                    <h2 className="text-3xl font-display font-bold text-slate-900 dark:text-white">Threat Intelligence</h2>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">Real-time overview of your email security status.</p>
                </div>
                <div className="flex gap-2">
                    <span className="text-sm font-medium text-slate-500">Last 7 Days</span>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                <StatsCard
                    title="Total Scans"
                    value={stats.total_scans}
                    icon={<Mail className="text-blue-500" />}
                    color="blue"
                />
                <StatsCard
                    title="Phishing Emails"
                    value={stats.phishing_email}
                    isBad={true}
                    icon={<AlertTriangle className="text-red-500" />}
                    color="red"
                />
                <StatsCard
                    title="Phishing SMS"
                    value={stats.phishing_sms}
                    isBad={true}
                    icon={<AlertTriangle className="text-red-500" />}
                    color="red"
                />
                <StatsCard
                    title="Phishing URLs"
                    value={stats.phishing_url}
                    isBad={true}
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
                    value={stats.phishing_email + stats.phishing_sms + stats.phishing_url > stats.legitimate_email + stats.legitimate_sms + stats.legitimate_url ? 'High' : 'Low'}
                    subtext={stats.total_scans > 0 ? 'System Healthy' : 'No Data'}
                    icon={<Globe className="text-indigo-500" />}
                    color="indigo"
                />
            </div>

            {/* Main Chart Section */}
            <div className="grid lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 card bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-soft border border-slate-200 dark:border-slate-700">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-6">Detection Trends</h3>
                    <div className="h-72 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={trendData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorPhishing" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#EF4444" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
                                    </linearGradient>
                                    <linearGradient id="colorLegit" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10B981" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8' }} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8' }} />
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                <Tooltip
                                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                                />
                                <Area type="monotone" dataKey="phishing" stroke="#EF4444" fillOpacity={1} fill="url(#colorPhishing)" />
                                <Area type="monotone" dataKey="legitimate" stroke="#10B981" fillOpacity={1} fill="url(#colorLegit)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="flex justify-end mt-6">
                      <button className="btn-primary px-6 py-2 text-sm" onClick={() => {
                        setSelectedReport({ chart: trendData });
                        setModalOpen(true);
                      }}>
                        View Full Report
                      </button>
                    </div>
                </div>

                <div className="card bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-soft border border-slate-200 dark:border-slate-700">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-6">Recent Alerts</h3>
                    <div className="space-y-4">
                        {stats.recent.map((scan, i) => (
                            <div key={scan.id || i} className="flex items-start gap-3 p-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors cursor-pointer">
                                <div className={`mt-1 min-w-[8px] h-2 w-2 rounded-full ${scan.result === 'Phishing' ? 'bg-red-500' : 'bg-emerald-500'}`}></div>
                                <div>
                                    <p className="text-sm font-medium text-slate-800 dark:text-slate-200">{scan.subject || 'No Subject'}</p>
                                    <p className="text-xs text-slate-500">{scan.email || 'Unknown sender'}</p>
                                </div>
                                <button className="btn-primary px-3 py-1 text-xs ml-4" onClick={() => {
                                  setSelectedReport(scan);
                                  setModalOpen(true);
                                }}>
                                  View Report
                                </button>
                            </div>
                        ))}
                    </div>
                    <button className="w-full mt-6 py-2 text-sm text-accent hover:text-accent-hover font-medium border border-accent/20 rounded-lg hover:bg-accent/5 transition-colors">
                        View All Alerts
                    </button>
                </div>
            </div>

            <ReportModal open={modalOpen} onClose={() => setModalOpen(false)} report={selectedReport} />
        </div>
    );
}

function StatsCard({ title, value, trend, icon, color, isBad, subtext }) {
    return (
        <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-soft border border-slate-200 dark:border-slate-700 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start">
                <div>
                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
                    <h3 className="text-3xl font-bold text-slate-900 dark:text-white mt-2">{value}</h3>
                </div>
                <div className={`p-3 rounded-xl bg-${color}-50 dark:bg-${color}-900/20`}>
                    {icon}
                </div>
            </div>
            {(trend || subtext) && (
                <div className="mt-4 flex items-center text-sm">
                    {trend && (
                        <span className={`font-medium ${isBad ? 'text-red-500' : 'text-emerald-500'}`}>
                            {trend}
                        </span>
                    )}
                    <span className="text-slate-400 ml-2">{subtext || 'vs last week'}</span>
                </div>
            )}
        </div>
    )
}

StatsCard.propTypes = {
    title: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    trend: PropTypes.string,
    icon: PropTypes.element.isRequired,
    color: PropTypes.string.isRequired,
    isBad: PropTypes.bool,
    subtext: PropTypes.string,
};

export default Dashboard;
