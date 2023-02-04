export function validator(field, type) {
  switch (type) {
    case "name":
      if (field.length <= 2 || field.length > 30) {
        let message = {
          name: "Bad Name",
        };
        throw message;
      }
      return true;
    case "email":
      if (field.length < 2 || field.length > 200) {
        let message = {
          email: "Short Email",
        };
        throw message;
      }
      if (
        !String(field)
          .toLowerCase()
          .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          )
      ) {
        let message = {
          password: "Wrong email",
        };
        throw message;
      }
      return true;
    case "password":
      if (field.length < 8) {
        let message = {
          password: "Too short password",
        };
        throw message;
      }
      return true;
    case "year":
      if (isNaN(parseInt(field))) {
        let message = {
          year: "Year should be Numeric like 2023",
        };
        throw message;
      }
      if (parseInt(field) > Date.getYear()) {
        let message = {
          year: "Wrong Year",
        };
        throw message;
      }
      return true;
    case "youtubeID":
      console.log(field.length);
      if (field.length !== 11) {
        let message = {
          link: "link shiuld have 11 characters for example HVHUjzZZGQ4",
        };
        throw message;
      }
      return true;
    default:
      return true;
  }
}
