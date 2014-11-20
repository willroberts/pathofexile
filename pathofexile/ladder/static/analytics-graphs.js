function drawAreDead(leagueId, elementId){
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Status');
            data.addColumn('number', 'Characters');

            $.get('/api/' + leagueId + '/are_dead', function (response) {
                var dataRows = [];
                var ladderSize = response['ladder_size'];
                dataRows.push(['Alive', ladderSize - response['are_dead']]);
                dataRows.push(['Dead', response['are_dead']]);


                data.addRows(dataRows);

                options = { title: 'Survival breakdown - '+leagueId,
                            width: 600,
                            height: 400
                            };

                var chart = new google.visualization.PieChart(document.getElementById(elementId));
                chart.draw(data, options);
            });
        }

function drawAreOnline(leagueId, elementId){
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Status');
            data.addColumn('number', 'Accounts');

            $.get('/api/' + leagueId + '/are_online', function (response) {
                var dataRows = [];
                var numAccounts = response['accounts'];
                dataRows.push(['Online', response['are_online']]);
                dataRows.push(['Offline', numAccounts - response['are_online']]);

                data.addRows(dataRows);

                options = { title: 'Accounts Online - '+leagueId,
                            width: 600,
                            height: 400
                            };

                var chart = new google.visualization.PieChart(document.getElementById(elementId));
                chart.draw(data, options);
            });
        }

function drawChallenges(leagueId, elementId){
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Challenges');
            data.addColumn('number', 'Accounts');

            $.get('/api/' + leagueId + '/challenge_breakdown', function (response) {
                var dataRows = [];
                for(var challengeNumber in response){
                    dataRows.push( [challengeNumber, response[challengeNumber]] );
                }
                data.addRows(dataRows);

                options = { title: 'Challenge breakdown - '+leagueId,
                            width: 600,
                            height: 400,
                            hAxis: {title: 'Challenges Completed'}
                            };

                var chart = new google.visualization.ColumnChart(document.getElementById(elementId));
                chart.draw(data, options);
            });
        }

function drawCharactersPerAccount(leagueId, elementId){
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Number of Characters');
            data.addColumn('number', 'Accounts');

            $.get('/api/' + leagueId + '/characters_per_account_breakdown', function (response) {
                var dataRows = [];
                for(var numCharacters in response){
                    dataRows.push( [numCharacters, response[numCharacters]] );
                }
                data.addRows(dataRows);

                options = { title: 'Characters per Account - ' + leagueId,
                            width: 600,
                            height: 400,
                            hAxis: {title: 'Number of Characters'}
                            };

                var chart = new google.visualization.ColumnChart(document.getElementById(elementId));
                chart.draw(data, options);
            });
        }

function drawClasses(leagueId, elementId){
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Class');
            data.addColumn('number', 'Characters');

            $.get('/api/' + leagueId + '/class_breakdown', function (response) {
                var dataRows = [];
                for(var className in response){
                    dataRows.push( [className, response[className]] );
                }
                data.addRows(dataRows);

                options = { title: 'Class breakdown - ' + leagueId,
                            width: 600,
                            height: 400
                            };

                var chart = new google.visualization.ColumnChart(document.getElementById(elementId));
                chart.draw(data, options);
            });
        }

function drawTwitchAccounts(leagueId, elementId){
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Status');
            data.addColumn('number', 'Characters');

            $.get('/api/' + leagueId + '/have_twitch_accounts', function (response) {
                var dataRows = [];
                var numAccounts = response['accounts'];
                dataRows.push(['Have Twitch Accounts', response['have_twitch_accounts']]);
                dataRows.push(['Don\'t Have Twitch Accounts', numAccounts - response['have_twitch_accounts']]);

                data.addRows(dataRows);

                options = { title: 'Twitch Accounts - ' + leagueId,
                            width: 600,
                            height: 400
                            };

                var chart = new google.visualization.PieChart(document.getElementById(elementId));
                chart.draw(data, options);
            });
        }

function drawLevelBreakdown(leagueId, elementId){
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Level');
            data.addColumn('number', 'Characters');

            $.get('/api/' + leagueId + '/level_breakdown', function (response) {
                var dataRows = [];
                for(var characterBin in response){

                    dataRows.push( [characterBin, response[characterBin]] );
                }
                data.addRows(dataRows);

                options = { title: 'Level breakdown - ' + leagueId,
                            width: 600,
                            height: 400,
                            hAxis: {title: 'Character Level'}
                            };

                var chart = new google.visualization.ColumnChart(document.getElementById(elementId));
                chart.draw(data, options);
            });
        }