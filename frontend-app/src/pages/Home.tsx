import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonSearchbar, IonList, IonItem, IonLabel, IonCard, IonCardHeader, IonCardTitle, IonCardSubtitle, IonCardContent, IonSpinner, IonText } from '@ionic/react';
import { useEffect, useState } from 'react';

// Define the structure of a Product
interface Product {
  id: number;
  name: string;
  description: string;
  category: string;
  brand: string;
  price: number;
  stock_quantity: number;
  sku: string;
}

// Custom hook for debouncing input
const useDebounce = (value: string, delay: number) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};


const Home: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const debouncedSearchQuery = useDebounce(searchQuery, 300); // 300ms delay

  const API_BASE_URL = 'http://127.0.0.1:5000'; // Flask backend URL

  useEffect(() => {
    // Function to fetch all products for the initial load
    const fetchInitialProducts = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/products`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: Product[] = await response.json();
        setProducts(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch products. Is the backend running?');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchInitialProducts();
  }, []);

  useEffect(() => {
    // Function to fetch products based on the search query
    const searchProducts = async () => {
      if (debouncedSearchQuery.trim() === '') {
        // If search is cleared, you might want to show all products again or an empty list.
        // For this example, we'll keep the initial list. Or fetch all again:
        // fetchInitialProducts(); 
        return;
      }
      
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/products/search?q=${encodeURIComponent(debouncedSearchQuery)}`);
        if (!response.ok) {
          throw new Error('Search request failed');
        }
        const data: Product[] = await response.json();
        setProducts(data);
        setError(null);
      } catch (err) {
        setError('Failed to perform search.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    // Trigger search only when the debounced query changes and is not empty
    if (debouncedSearchQuery) {
      searchProducts();
    }
  }, [debouncedSearchQuery]);


  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Product Search</IonTitle>
        </IonToolbar>
        <IonToolbar>
          <IonSearchbar
            placeholder="Search by Name, SKU, Brand..."
            value={searchQuery}
            onIonInput={(e) => setSearchQuery(e.detail.value!)}
            debounce={0} // We handle debouncing manually with our hook
          ></IonSearchbar>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        {loading && <div className="ion-text-center"><IonSpinner /></div>}
        {error && <IonText color="danger"><p className="ion-text-center">{error}</p></IonText>}
        {!loading && !error && (
          <IonList>
            {products.length > 0 ? products.map((product) => (
              <IonCard key={product.id}>
                <IonCardHeader>
                  <IonCardTitle>{product.name}</IonCardTitle>
                  <IonCardSubtitle>{product.brand} - {product.category}</IonCardSubtitle>
                </IonCardHeader>
                <IonCardContent>
                  <p>{product.description}</p>
                  <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
                  <p><strong>Stock:</strong> {product.stock_quantity} units</p>
                  <p><strong>SKU:</strong> {product.sku}</p>
                </IonCardContent>
              </IonCard>
            )) : (
              <IonItem lines="none">
                <IonLabel className="ion-text-center">No products found.</IonLabel>
              </IonItem>
            )}
          </IonList>
        )}
      </IonContent>
    </IonPage>
  );
};

export default Home;