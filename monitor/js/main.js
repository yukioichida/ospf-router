var app = angular.module("monitor", []);

app.controller("MonitorCtrl", function($scope, $http){
  $scope.title = "Trabalho Redes - Monitor";

  $scope.orderBy = function(type){
    $scope.orderByType = type;
    $scope.direction = !$scope.direction;
  }
  $scope.requires = [];
  $scope.update = function(){
    var mydata = JSON.parse(data);
    console.log(mydata);
    $scope.requires = mydata;
  }
  $scope.update();
});
