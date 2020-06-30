import React, { useState, useEffect } from 'react'
import Product from '../../components/Product/Product'
import axios from 'axios'


export default function App() {
  const [products, setProducts] = useState([])
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/products/')
      .then((response) => setProducts(response.data))
  }, [])
  return (
    <>
      {
        products.map((product) => {
          return (
            <Product key={product.id} id={product.id} user_id={product.user} title={product.title} description={product.description} date={product.date} />
          )
        })
      }
    </>
  )
}