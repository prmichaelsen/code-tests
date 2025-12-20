# Map Search Test

🌐 **Live Demo**: https://master.map-search-app.pages.dev/

---

# Map Search Test

## Base Files

You've been given:

1. `index.html`: The base HTML file with a full-page Google Map
2. `main.css`: The base CSS file
3. `main.js`: The base JS file
4. `sample-data.js`: The sample data that should be searched. Each record has _at least_ an `id` and `name`.
5. `icon-search.svg` & `icon-pin.svg`: SVG's to use in your design _(see the provided designs below)_

## The Task

We use [React](https://react.dev/) for our user interface at **Ground Signal**

Create a user interface **that resembles the images below** in React as closely as possible and implements the
following:

1. "Autocomplete" search field - Using the provided sample data in `sample-data.js`, allow users to search in an input
   field for results based on the data `name` value.
2. Results list - Show the results of the autocomplete search as a list of items that a user can select/click.
3. Locations/markers - When a user finds and clicks a search result, display the location on the map.
4. Details modal - When a user clicks a map location/marker, display a modal that contains additional information about
   that location. (see below)
5. Star a location - Save the result to a list and share the list with anyone.
6. Data need to be hosted from a mock api server. Implement basic CRUD, adding/edit/remove for new location (title,
   description, images, link …etc) as applicable.

**How the initial page should look:**

![The initial user interface](./test-example-start.png?raw=true)

### Search Field

When entering a query into the search field the matching results should populate an area below the search **as a user
types**. If no results are found, make sure to show a message letting a user know that :) _Nothing is worse than
thinking it's trying to load forever!_

**How the search interface should look:**

![Search results](./test-example-search.png?raw=true)

### Details Modal

When clicking on a map location/marker you should display a modal that contains information about that specific
location. **This modal should be both horizontally and vertically aligned.**

**How the modal should look - _(ignore the vertical line guides in your design)_:**

![Vertically and horizontally aligned modal](./test-example-modal.png?raw=true)

## Things to think about

* Document your code! This is your opportunity to help us understand you. Let us know:
    * why you did (or did not) do something,
    * why you used (or did not use) any frameworks/libraries,
    * what you wanted to do, but could not because...?
* How close does your final design match the provided images above?

## Extra Credit

* We also implement _lots_ of charts using [Chart.js](http://chartjs.org/). We've included some data (
  see `avgStoreTraffic`) in the `sample-data.js` in case you want to spice up your modal with that.
* Let us know how we could improve this test. Bug? Improvement? Send us a pull request!
* Anything else awesome. :)

## Be Unique!

If you have any questions/comments/feedback, don't hesitate to [shoot us an email](mailto:jobs@groundsignal.com)!

For quick reference, some Google Maps documentation can be found
at [https://developers.google.com/maps/documentation/javascript/](https://developers.google.com/maps/documentation/javascript)
