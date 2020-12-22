# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import glob
import os
import sys

import pytest

from pytorch_lightning import Trainer
from tests import LEGACY_PATH

LEGACY_CHECKPOINTS_PATH = os.path.join(LEGACY_PATH, 'checkpoints')
CHECKPOINT_EXTENSION = ".ckpt"


@pytest.mark.parametrize("pl_version", ["1.0.0", "1.0.1", "1.0.2"])
def test_resume_legacy_checkpoints(tmpdir, pl_version):
    path_dir = os.path.join(LEGACY_CHECKPOINTS_PATH, pl_version)

    # todo: make this as mock, so it is cleaner...
    orig_sys_paths = list(sys.path)
    sys.path.insert(0, path_dir)
    from zero_training import DummyModel

    path_ckpts = sorted(glob.glob(os.path.join(path_dir, f'*{CHECKPOINT_EXTENSION}')))
    assert path_ckpts, 'No checkpoints found in folder "%s"' % path_dir
    path_ckpt = path_ckpts[-1]

    model = DummyModel.load_from_checkpoint(path_ckpt)
    trainer = Trainer(default_root_dir=tmpdir, max_epochs=6)
    result = trainer.fit(model)
    assert result

    # todo
    # model = DummyModel()
    # trainer = Trainer(default_root_dir=tmpdir, max_epochs=1, resume_from_checkpoint=path_ckpt)
    # result = trainer.fit(model)
    # assert result

    sys.path = orig_sys_paths