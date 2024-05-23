<template>
  <div class="row">
    <div class="col-sm-6 mb-3 mb-sm-0">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Click to manage items</h5>
          <p class="card-text">
            Manager can create new item, update existing items or delete items
          </p>
          <router-link to="/manager-item" class="btn btn-primary"
            >Manage items</router-link
          >
        </div>
      </div>
    </div>
    <div class="col-sm-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Download CSV</h5>
          <p class="card-text">Click here to download csv report</p>
          <button @click="exportCSV" class="btn btn-primary">
            Download CSV
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from "@/axios";

export default{
  created(){
    console.log("hello")
  },
  methods:{
    save(filename, data) {
     const blob = new Blob([data], {type: 'text/csv'});
     if(window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveBlob(blob, filename);
     }
     else{
        const elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(blob);
        elem.download = filename;        
        document.body.appendChild(elem);
        elem.click();        
        document.body.removeChild(elem);
     }
    },
    async exportCSV(){
      const response=await axios.get("/export-csv");
      console.log(response.data);
      this.downloadCSV(response.data["id"]);
    },
    async downloadCSV(id){
      const response=await axios.get("/download-csv?id="+id);
      const status= response.data["status"];
      if (status=="SUCCESS") {
        this.save(new Date()+".csv",response.data["data"])
      } 
      else{
        setTimeout(this.downloadCSV(id),10000)
      }
    }

  }
}


</script>
  
<style>
</style>