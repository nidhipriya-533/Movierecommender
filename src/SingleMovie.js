import { NavLink, useParams } from "react-router-dom";
// import Footer from "./footer";
import useFetch from "./useFetch";
import MovieRecommendations from './MovieRecommendations';

const SingleMovie = () => {
  const { id } = useParams();
  console.log(id);

  const { isLoading, movie} = useFetch(`&i=${id}`);

  


  if (isLoading) {
    return (
      <section className="movie-section ">
        <div className="loading">Loading....</div>;
      </section>
    );
  }

  return (<>
    <section className="movie-section" style={{
      backgroundImage: `url(${movie.Poster})`
    }}>
      <div className="movie-card">
        <figure>
          <img src={movie.Poster} alt="" />
        </figure>
        <div className="card-content">
          <p className="title">{movie.Title}</p>
          <p className=""></p>
          <p className="card-text">{movie.Released}</p>
          <p className="card-text">{movie.Genre}</p>
          <p className="card-text">{movie.imdbRating} / 10</p>
          <p className="card-text">{movie.Country}</p>
          <NavLink to="/" className="back-btn">
            Go Back
          </NavLink>
        </div>
        
      </div>
      <MovieRecommendations />
      

    </section>
    
    </>
  );
};

export default SingleMovie;








