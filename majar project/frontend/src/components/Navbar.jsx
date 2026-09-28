export default function Navbar({ page, setPage }) {
  return <nav className="nav"><button className="brand" onClick={() => setPage('home')}>◈ Sentiment<span>AI</span></button><div className="navlinks">{['home', 'dashboard', 'reviews'].map(item => <button className={page === item ? 'active' : ''} onClick={() => setPage(item)} key={item}>{item[0].toUpperCase() + item.slice(1)}</button>)}</div></nav>
}
