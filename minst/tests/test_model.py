import pytest

import os
import pandas as pd

import minst.model as model


@pytest.fixture
def raw_obs(rwc_root):
    afile = os.path.join(rwc_root, "RWC_I_01/011/011PFNOP.flac")
    return dict(index='U1309f091', dataset='uiowa', audio_file=afile,
                instrument='piano', source_index='U12345',
                start_time=0.0, duration=2, note_number=45,
                dynamic='pp', partition='test-0')


@pytest.fixture
def test_obs():
    obs = [
        dict(index="abc123", dataset="rwc", audio_file="foo_00.aiff",
             instrument="tuba", source_index="001", start_time=None,
             duration=None, note_number="A4", dynamic="pp", partition=None),
        dict(index="abc234", dataset="uiowa", audio_file="foo_01.aiff",
             instrument="horn-french", source_index="001", start_time=None,
             duration=None, note_number="A4", dynamic="pp", partition=None),
        dict(index="def123", dataset="philharmonia", audio_file="foo_02.aiff",
             instrument="tuba", source_index="001", start_time=None,
             duration=None, note_number="A4", dynamic="pp", partition=None)
    ]
    return obs


def test_Observation___init__(raw_obs):
    obs = model.Observation(**raw_obs)
    assert obs


def test_Observation_to_builtin(raw_obs):
    obs = model.Observation(**raw_obs)
    assert obs.to_builtin() == raw_obs


def test_Observation_from_series(test_obs):
    index = [x.pop('index') for x in test_obs]
    df = pd.DataFrame.from_records(test_obs, index=index)
    # import pdb;pdb.set_trace()
    obs = model.Observation.from_series(df.ix[0])
    assert obs.index == index[0]
    assert obs.instrument == 'tuba'


def test_Observation_to_series(raw_obs):
    obs = model.Observation(**raw_obs)
    rec = obs.to_series()
    assert rec.name == raw_obs['index']
    assert rec.instrument == raw_obs['instrument']


def test_Observation_to_dict(raw_obs):
    obs = model.Observation(**raw_obs)
    rec_obs = obs.to_dict()
    assert rec_obs == raw_obs


def test_Observation___get_item__(raw_obs):
    obs = model.Observation(**raw_obs)
    assert obs['index'] == obs.index == raw_obs['index']


def test_Observation_validate(raw_obs):
    obs = model.Observation(**raw_obs)
    assert obs.SCHEMA

    assert obs.validate()
    raw_obs['audio_file'] = ("dummy_philharmonia/www.philharmonia.co.uk/"
                             "assets/audio/samples/instruments/cello.zip")
    obs = model.Observation(**raw_obs)
    assert not obs.validate()


def test_Collection___init__(raw_obs):
    obs = model.Observation(**raw_obs)
    dset = model.Collection([obs])
    assert len(dset) == 1


def test_Collection_to_dataframe(raw_obs):
    obs = model.Observation(**raw_obs)
    dset = model.Collection([obs]).to_dataframe()
    assert len(dset) == 1
    assert dset.index[0] == obs.index


def test_Collection_view(test_obs):
    ds = model.Collection(test_obs)
    rwc_view = ds.view("rwc")
    assert set(rwc_view["dataset"].unique()) == set(["rwc"])
