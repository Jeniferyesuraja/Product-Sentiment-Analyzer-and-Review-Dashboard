import { NavLink } from 'react-router-dom'

const groups = [
  { label: 'Workspace', items: [['/', 'Home', '⌂'], ['/dashboard', 'Dashboard', '▦'], ['/products', 'Products', '□'], ['/product-search', 'Product Search', '⌕'], ['/reviews', 'Reviews', '≡']] },
  { label: 'Intelligence', items: [['/sentiment', 'Sentiment Analysis', '✦'], ['/analytics', 'Analytics', '◒'], ['/trends', 'Trends', '↗'], ['/scraper', 'Scraper', '⇩']] },
  { label: 'Manage', items: [['/reports', 'Reports', '▤'], ['/history', 'History', '◷'], ['/favorites', 'Favorites', '♡']] },
  { label: 'System', items: [['/settings', 'Settings', '⚙'], ['/help', 'Help & Docs', '?']] },
]

export default function Sidebar({ open, close }) {
  return <aside className={`sidebar ${open ? 'open' : ''}`}><div className="side-brand"><span>◈</span> Sentiment<span>AI</span><button onClick={close} aria-label="Close navigation">×</button></div>{groups.map(group => <div className="nav-group" key={group.label}><small>{group.label}</small>{group.items.map(([to, label, icon]) => <NavLink end={to === '/'} to={to} key={to} onClick={close}><b>{icon}</b>{label}</NavLink>)}</div>)}<div className="side-status"><i /> Demo mode active<small>MongoDB ready when configured</small></div></aside>
}
