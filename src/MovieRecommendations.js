import Footer from "./footer";
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useFetch from './useFetch';
import { useGlobalContext } from './context';

const MovieRecommendations = () => {
  const { id } = useParams();
  const { isLoading, movie, isError } = useFetch(`i=${id}`);
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);
  const { setQuery } = useGlobalContext();
  const navigate = useNavigate();

  useEffect(() => {
    if (movie && movie.Title) {
      const fetchRecommendations = async () => {
        try {
          const response = await fetch(`https://nidhipriya533-movierecommender.hf.space/${movie.Title}`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          const movieDetails = await Promise.all(
            data.Recommendations.map(async (recMovie) => {
              const res = await fetch(`http://www.omdbapi.com/?apikey=8e35932b&s=${recMovie}`); //omdb
              const recMovieData = await res.json();
              return recMovieData.Search[0];
            })
          );
          setRecommendations(movieDetails);
          setError(null);
        } catch (error) {
          setError(error.toString());
        }
      };

      fetchRecommendations();
    }
  }, [movie]);

  const handlePosterClick = (recMovieTitle) => {
    setQuery(recMovieTitle);
    navigate('/');
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError.show === "true") {
    return <div>Error: {isError.msg}</div>;
  }

  return (
    <div>
      <h1 className='movietext'><p>Movie Recommendations for {movie?.Title}</p></h1>
      {error && <p>Error: {error}</p>}
      <ul className="recommendations-container">
        {recommendations.map((recMovie, index) => (
          <li key={index} className="recommendation-item">
            <h3>{recMovie.Title}</h3>
            {recMovie.Poster && (
              <img
                src={recMovie.Poster}
                alt={recMovie.Title}
                onClick={() => handlePosterClick(recMovie.Title)}
              />
            )}
          </li>
        ))}
      </ul>
      <Footer />
    </div>
  );
};

export default MovieRecommendations;
