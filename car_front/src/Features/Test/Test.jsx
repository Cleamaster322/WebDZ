import { useState, useEffect } from 'react'

import axios from 'axios'
import api from "../../shared/api.jsx";

function Test() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        api
          .get('/cars/test/')
          .then(response => {
            console.log(response)
            setData(response)
          })
          .catch(error => console.error(error))

        api
            .post('cars/test1/', {'name':123})
            .then(response => {
              console.log(response)
            })
      } catch (err) {
        setError(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error ^_^</div>

  return (
    <>
      <div>{data}</div>
    </>
  )
}
export default Test