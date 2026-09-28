import { Component, useEffect, useState } from 'react'
import { Navigate, Route, Routes, useNavigate, useParams } from 'react-router-dom'
import { getOverview, getProducts, getReviews, searchProduct, toggleFavorite } from './services/api'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import Loading from './components/Loading'
import ReviewCard from './components/ReviewCard'
import WorkspacePage from './pages/WorkspacePage'

const demoProducts = [
	{ _id: 'demo-iphone', name: 'iPhone 15', source: 'Demo catalog', rating: 4.2, review_count: 20, sentiment: 'Positive' },
	{ _id: 'demo-samsung', name: 'Samsung Galaxy S24', source: 'Demo catalog', rating: 4.1, review_count: 20, sentiment: 'Positive' },
	{ _id: 'demo-oneplus', name: 'OnePlus 12', source: 'Demo catalog', rating: 3.8, review_count: 20, sentiment: 'Positive' },
	{ _id: 'demo-dell', name: 'Dell Laptop', source: 'Demo catalog', rating: 3.6, review_count: 20, sentiment: 'Neutral' },
	{ _id: 'demo-sony', name: 'Sony Headphones', source: 'Demo catalog', rating: 4.4, review_count: 20, sentiment: 'Positive' },
]

const demoOverview = { total_products: demoProducts.length, total_reviews: 100, positive: 62, negative: 18, neutral: 20, average_rating: 4.02 }

function Shell() {
	const navigate = useNavigate()
	const [open, setOpen] = useState(false)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState('')
	const [overview, setOverview] = useState(null)
	const [products, setProducts] = useState([])
	const [reviews, setReviews] = useState([])
	const refresh = async () => { try { const [overviewResult, productsResult, reviewsResult] = await Promise.all([getOverview(), getProducts(), getReviews()]); setOverview(overviewResult.data?.total_products ? overviewResult.data : demoOverview); setProducts(productsResult.data?.products?.length ? productsResult.data.products : demoProducts); setReviews(reviewsResult.data?.reviews || []) } catch (err) { setOverview(demoOverview); setProducts(demoProducts); setReviews([]); setError(err.response?.data?.error || 'Unable to connect to Flask API. Showing demo data.') } finally { setLoading(false) } }
	useEffect(() => { refresh() }, [])
	const analyze = async product => { if (!product?.trim()) return; setLoading(true); setError(''); try { await searchProduct(product); await refresh(); navigate('/dashboard') } catch (err) { setError(err.response?.data?.error || 'Analysis failed.') } finally { setLoading(false) } }
	const favorite = async product => { try { await toggleFavorite({ name: product.name, rating: product.rating || 0, review_count: product.review_count || 0 }); setError('') } catch (err) { setError('Could not update favorites.') } }
	const pageProps = { overview, products, reviews, onAnalyze: analyze, onFavorite: favorite }
	return <div className="app-shell"><Sidebar open={open} close={() => setOpen(false)} /><div className="main-area"><Topbar onMenu={() => setOpen(true)} onSearch={analyze} /><main className="content"><ErrorBoundary><>{error && <div className="error">{error}<button onClick={refresh}>Retry</button></div>}{loading ? <Loading /> : <Routes><Route path="/" element={<WorkspacePage name="home" {...pageProps} />} /><Route path="/dashboard" element={<WorkspacePage name="dashboard" {...pageProps} />} /><Route path="/products/:id" element={<ProductDetails products={products} reviews={reviews} onAnalyze={analyze} />} /><Route path="/products" element={<WorkspacePage name="products" {...pageProps} />} /><Route path="/product-search" element={<WorkspacePage name="product-search" {...pageProps} />} /><Route path="/reviews" element={<WorkspacePage name="reviews" {...pageProps} />} /><Route path="/sentiment" element={<WorkspacePage name="sentiment" {...pageProps} />} /><Route path="/analytics" element={<WorkspacePage name="analytics" {...pageProps} />} /><Route path="/trends" element={<WorkspacePage name="trends" {...pageProps} />} /><Route path="/scraper" element={<WorkspacePage name="scraper" {...pageProps} />} /><Route path="/reports" element={<WorkspacePage name="reports" {...pageProps} />} /><Route path="/history" element={<WorkspacePage name="history" {...pageProps} />} /><Route path="/favorites" element={<WorkspacePage name="favorites" {...pageProps} />} /><Route path="/settings" element={<WorkspacePage name="settings" {...pageProps} />} /><Route path="/help" element={<WorkspacePage name="help" {...pageProps} />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>}</></ErrorBoundary></main><footer>SentimentAI <span>Product intelligence, made legible.</span></footer></div></div>
}
class ErrorBoundary extends Component { state = { hasError: false }; static getDerivedStateFromError() { return { hasError: true } } componentDidCatch(error) { console.error(error) } render() { return this.state.hasError ? <div className="empty-card"><span>!</span><h3>This page could not be rendered.</h3><p>Refresh the page and try again.</p><button className="primary" onClick={() => window.location.reload()}>Retry</button></div> : this.props.children } }
function ProductDetails({ products, reviews, onAnalyze }) { const { id } = useParams(); const product = products.find(item => item._id === id); const productReviews = reviews.filter(item => item.product === product?.name).slice(0, 4); if (!product) return <div className="empty-card"><h3>Product not found</h3></div>; return <><div className="section-head"><div><p className="eyebrow">PRODUCT / DETAILS</p><h1>{product.name}</h1></div><button className="primary" onClick={() => onAnalyze(product.name)}>Analyze reviews</button></div><div className="feature-banner"><div><p className="eyebrow">{product.source || 'CATALOG PRODUCT'}</p><h2>★ {product.rating || 0} average rating</h2><p>{product.review_count || 0} reviews indexed with {product.sentiment || 'Neutral'} as the leading sentiment.</p></div><span className="banner-icon">{product.name.slice(0, 2).toUpperCase()}</span></div><h2 className="subheading">Recent reviews</h2><div className="review-grid">{productReviews.map((review, index) => <ReviewCard review={review} key={review._id || index} />)}</div></> }
export default Shell
